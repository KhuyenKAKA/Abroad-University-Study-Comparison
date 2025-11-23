import json

with open("raw_data_visualize.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def build_summary(item):
    title = item.get("title", "N/A")
    rank = item.get("rank_display", "N/A")
    score = item.get("overall_score", "N/A")
    country = item.get("country", "")
    city = item.get("city", "")
    region = item.get("region", "")

    lines = []
    lines.append(f"{title} là một trường đại học tại {city}, {country} ({region}).")
    lines.append(f"Trường có xếp hạng QS: {rank}, điểm tổng: {score}/100.")

    # more_info
    for info in item.get("more_info", []):
        lbl = info.get("label", "")
        val = info.get("value", "")
        if val and "Generate" not in val:
            lines.append(f"{lbl}: {val}.")

    # scores
    scores = item.get("scores", {})
    if isinstance(scores, dict):
        lines.append("Các chỉ số chi tiết:")
        for category, indicators in scores.items():
            lines.append(f"- Nhóm {category}:")
            for ind in indicators:
                name = ind.get("indicator_name", "")
                s = ind.get("score", "")
                r = ind.get("rank", "")
                lines.append(f"  + {name}: Điểm {s}, hạng {r}.")

    lines.append("Tóm lại, đây là lựa chọn tốt cho sinh viên quốc tế cần môi trường học thuật mạnh.")
    return " ".join(lines)

examples = []

for item in data[:300]: 
    title = item.get("title")
    if not title:
        continue

    user_q = f"Hãy giới thiệu chi tiết về trường {title} cho học sinh Việt Nam."
    answer = build_summary(item)

    examples.append({
        "systemInstruction": {
            "role": "system",
            "parts": [{"text": "Bạn là cố vấn du học quốc tế."}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": user_q}]},
            {"role": "model", "parts": [{"text": answer}]}
        ]
    })

with open("train_university_chatbot.jsonl", "w", encoding="utf-8") as f:
    for ex in examples:
        f.write(json.dumps(ex, ensure_ascii=False) + "\n")

print("Done! train_university_chatbot.jsonl created.")
