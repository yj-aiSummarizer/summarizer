from chains.summarize_chain import get_summary_chain
from chains.translate_chain import translate_node_ko

def get_summary_and_translate_chain(mode: str = "detailed", lang: str = "ko"):
    summary_chain = get_summary_chain(mode)

    if lang == "ko":
        return summary_chain | translate_node_ko
    else:
        return summary_chain
