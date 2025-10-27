
import datetime
def render_markdown(summary:dict)->str:
    lines = []
    lines.append(f"# Commercialisation Summary — {summary.get('project_name','Untitled Project')}")
    lines.append(f"_Generated: {datetime.date.today().isoformat()}_\n")
    lines.append("## TRL Assessment")
    lines.append(f"- Estimated TRL: **{summary.get('trl','N/A')}**\n")
    lines.append("## Top 3 Recommended Business Models")
    for i, bm in enumerate(summary.get('top_models',[]), start=1):
        lines.append(f"{i}. **{bm['name']}** — {bm.get('why','Fit based on profile and TRL')}" )
    fin = summary.get('finance',{})
    lines.append("\n## Financial Snapshot")
    lines.append(f"- NPV: **{fin.get('npv','N/A')}**" )
    lines.append(f"- IRR: **{fin.get('irr','N/A')}**" )
    lines.append(f"- Payback: **{fin.get('payback','N/A')} years**\n" )
    if summary.get('notes'):
        lines.append("## Notes")
        lines.append(summary['notes'])
    return "\n".join(lines)
