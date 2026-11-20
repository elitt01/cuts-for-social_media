#!/usr/bin/env python3
"""Rank editorial candidates without representing a heuristic as viral probability."""

import argparse
import copy
import datetime as dt
import json
import math
from pathlib import Path
import sys
from urllib.parse import urlparse


WEIGHTS = {"gancho": 20, "desfecho": 20, "compreensao": 15,
           "adequacao": 15, "relevancia": 10, "novidade": 10, "viabilidade": 10}
HEURISTIC_VERSION = "0.1"


def fail(path, message):
    raise ValueError(f"{path}: {message}")


def number(value, path):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        fail(path, "esperado número finito não negativo")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite or value < 0:
        fail(path, "esperado número finito não negativo")
    return value


def nonempty(value, path):
    if not isinstance(value, str) or not value.strip():
        fail(path, "esperado texto não vazio")
    return value


def timestamp(value, path):
    nonempty(value, path)
    try:
        result = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail(path, "esperado timestamp ISO-8601 com fuso")
    if result.utcoffset() is None:
        fail(path, "timestamp precisa de fuso")
    return result


def performance(candidate, path):
    original = candidate.get("observed_performance")
    if original is None:
        original = {}
    if not isinstance(original, dict):
        fail(path, "esperado objeto")
    snapshots = original.get("snapshots", [])
    if not isinstance(snapshots, list):
        fail(f"{path}.snapshots", "esperada lista")
    observed = False
    for index, snapshot in enumerate(snapshots):
        item_path = f"{path}.snapshots[{index}]"
        if not isinstance(snapshot, dict):
            fail(item_path, "esperado objeto")
        timestamp(snapshot.get("observed_at"), f"{item_path}.observed_at")
        for key in ("views", "likes", "comments", "shares", "saves"):
            value = snapshot.get(key)
            if value is not None:
                if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                    fail(f"{item_path}.{key}", "esperada contagem inteira não negativa ou null")
                observed = True
    return {
        "label": "tracao_observada_sem_base" if observed else "desempenho_desconhecido",
        "snapshots": copy.deepcopy(snapshots),
        "comparison_cohort": copy.deepcopy(original.get("comparison_cohort")),
        "comparison_status": "not_evaluated",
    }


def evaluate(candidate, index):
    path = f"candidates[{index}]"
    if not isinstance(candidate, dict):
        fail(path, "esperado objeto")
    candidate_id = nonempty(candidate.get("candidate_id"), f"{path}.candidate_id")
    potential = candidate.get("potential", {})
    if not isinstance(potential, dict):
        fail(f"{path}.potential", "esperado objeto")
    criteria = potential.get("criteria", {})
    if not isinstance(criteria, dict):
        fail(f"{path}.potential.criteria", "esperado objeto")
    extra = set(criteria) - set(WEIGHTS)
    if extra:
        fail(f"{path}.potential.criteria", f"critérios desconhecidos: {', '.join(sorted(extra))}")
    normalized, missing, lower, unknown_weight = {}, [], 0.0, 0
    for key, weight in WEIGHTS.items():
        item = criteria.get(key)
        criterion_path = f"{path}.potential.criteria.{key}"
        if item is None:
            normalized[key] = None
            missing.append(key)
            unknown_weight += weight
            continue
        if not isinstance(item, dict):
            fail(criterion_path, "usar objeto score/evidence/timecode_seconds ou null")
        score = item.get("score")
        if isinstance(score, bool) or not isinstance(score, int) or not 0 <= score <= 4:
            fail(f"{criterion_path}.score", "esperado inteiro de 0 a 4")
        evidence = nonempty(item.get("evidence"), f"{criterion_path}.evidence")
        timecode = number(item.get("timecode_seconds"), f"{criterion_path}.timecode_seconds")
        normalized[key] = {"score": score, "evidence": evidence, "timecode_seconds": timecode}
        lower += weight * score / 4
    complete = not missing
    final_score = lower if complete else None
    reasons = []
    source_url = candidate.get("source_url")
    source_file = candidate.get("source_file")
    if source_url is not None:
        nonempty(source_url, f"{path}.source_url")
        parsed = urlparse(source_url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            fail(f"{path}.source_url", "esperada URL http(s)")
    if source_file is not None:
        nonempty(source_file, f"{path}.source_file")
    if not source_url and not source_file:
        reasons.append("fonte_nao_informada")
    start = candidate.get("source_start_seconds")
    end = candidate.get("source_end_seconds")
    for key, value in (("source_start_seconds", start), ("source_end_seconds", end)):
        if value is not None:
            number(value, f"{path}.{key}")
    if start is None or end is None:
        reasons.append("intervalo_do_corte_incompleto")
    elif end <= start:
        fail(path, "source_end_seconds deve ser maior que source_start_seconds")
    else:
        for key, item in normalized.items():
            if item is not None and not start <= item["timecode_seconds"] <= end:
                fail(f"{path}.potential.criteria.{key}.timecode_seconds", "fora do intervalo do corte")
    context = candidate.get("context_reviewed", {})
    if not isinstance(context, dict):
        fail(f"{path}.context_reviewed", "esperado objeto")
    mode = context.get("mode", "unavailable")
    if mode not in ("audiovisual", "transcript_only", "unavailable"):
        fail(f"{path}.context_reviewed.mode", "modo desconhecido")
    context_start, context_end = context.get("start_seconds"), context.get("end_seconds")
    for key, value in (("start_seconds", context_start), ("end_seconds", context_end)):
        if value is not None:
            number(value, f"{path}.context_reviewed.{key}")
    if context_start is not None and context_end is not None and context_end <= context_start:
        fail(f"{path}.context_reviewed", "end_seconds deve ser maior que start_seconds")
    if mode != "audiovisual":
        reasons.append("inspecao_audiovisual_pendente")
    if context_start is None or context_end is None:
        reasons.append("intervalo_do_contexto_incompleto")
    elif start is not None and end is not None and not (context_start <= start and context_end >= end):
        reasons.append("contexto_nao_cobre_o_corte")
    if not complete:
        reasons.append("avaliacao_incompleta")
    for key in ("gancho", "desfecho", "viabilidade"):
        item = normalized[key]
        if item is not None and item["score"] < 2:
            reasons.append(f"{key}_abaixo_do_minimo")
    if complete and final_score < 65:
        reasons.append("potencial_abaixo_de_65")
    eligible = not reasons
    tier = None if not complete else ("priorizar" if final_score >= 80 else
                                     "considerar_com_ajuste" if final_score >= 65 else "nao_priorizar")
    return {
        "candidate_id": candidate_id,
        "source_url": source_url,
        "source_file": source_file,
        "source_start_seconds": start,
        "source_end_seconds": end,
        "context_reviewed": copy.deepcopy(context),
        "potential": {
            "heuristic_version": HEURISTIC_VERSION,
            "assessment_status": "complete" if complete else "incomplete",
            "criteria": normalized,
            "score": final_score,
            "range_min": lower,
            "range_max": lower + unknown_weight,
            "evidence_coverage_pct": 100 - unknown_weight,
            "tier": tier,
        },
        "observed_performance": performance(candidate, f"{path}.observed_performance"),
        "selection_eligible": eligible,
        "selection_blockers": reasons,
    }


def rank_candidates(payload):
    candidates = payload.get("candidates") if isinstance(payload, dict) else payload
    if not isinstance(candidates, list):
        fail("input", "esperada lista de candidatos ou objeto com candidates")
    results = [evaluate(candidate, index) for index, candidate in enumerate(candidates)]
    ids = [result["candidate_id"] for result in results]
    if len(ids) != len(set(ids)):
        fail("input", "candidate_id duplicado")
    # Unknown upper bounds never determine winners or imply established quality.
    def order(item):
        p = item["potential"]
        group = 0 if item["selection_eligible"] else 1 if p["score"] is not None else 2
        return group, -p["range_min"], -p["evidence_coverage_pct"], item["candidate_id"]
    results.sort(key=order)
    selected = next((item["candidate_id"] for item in results if item["selection_eligible"]), None)
    return {
        "schema_version": "0.1.0",
        "heuristic_version": HEURISTIC_VERSION,
        "weights": WEIGHTS,
        "interpretation": "Potencial editorial heurístico; não é probabilidade de viralização.",
        "status": "selected" if selected is not None else "research_required",
        "selected_candidate_id": selected,
        "candidates": results,
    }


def reject_constant(value):
    raise ValueError(f"constante JSON inválida: {value}")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            fail("JSON", f"campo duplicado: {key}")
        result[key] = value
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON de candidatos")
    parser.add_argument("--output", type=Path, help="Salvar resultado JSON; omitir para stdout")
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"), parse_constant=reject_constant,
                             object_pairs_hook=unique_object)
        result = rank_candidates(payload)
        encoded = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            args.output.write_text(encoded, encoding="utf-8")
        else:
            sys.stdout.write(encoded)
    except (OSError, ValueError, TypeError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
