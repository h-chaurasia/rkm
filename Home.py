import streamlit as st

from common import APP_TITLE, render_footer, render_header

st.set_page_config(page_title=APP_TITLE, page_icon="static/images/icar_1.png", layout="centered")

render_header()

st.markdown(
    """
### What is Yarn Tenacity?

**Tenacity** is the strength of a yarn relative to its thickness — the force a yarn can
withstand before breaking, per unit of its linear density. It is commonly expressed as
**Rkm** (breaking length in kilometers) or in g/tex. Unlike a simple breaking-load number,
tenacity lets mills compare the strength of yarns of different counts on equal footing.

### Why does it matter?

Tenacity is one of the most critical quality parameters in the cotton-to-fabric value chain:

- **Spinning performance** — low-tenacity yarn breaks more often on the spinning frame,
  increasing downtime and reducing productivity.
- **Weaving and knitting efficiency** — weak yarn causes warp/weft breaks, slowing looms
  and knitting machines and raising rejection rates.
- **Fabric quality** — the strength and durability of the final fabric depend directly on
  the tenacity of the yarn it is made from.
- **Cost control** — identifying weak yarn batches early avoids wasted processing time and
  raw material further down the chain.

Traditionally, tenacity can only be measured *after* yarn has actually been spun and tested
on a strength tester — a process that takes time and consumes material.

### What this webapp does

This tool predicts yarn **Tenacity (Rkm)** directly from the cotton fiber properties
measured by a standard HVI (High Volume Instrument) test — **UHML, Uniformity Index (UI),
Micronaire (Mic), Fiber Strength (Str), Elongation (E)** — together with the intended
**yarn count**. It uses a machine learning model trained on historical spinning data by
**ICAR-CIRCOT**, so you can estimate the tenacity a yarn will achieve *before* it is spun,
helping with raw material selection, mixing decisions, and quality planning.

Head to the **Prediction** page in the sidebar to try it — either enter a single set of
fiber properties, or upload a CSV of many samples at once.
"""
)

st.page_link("pages/1_Prediction.py", label="Go to Prediction →", icon="🔮")

render_footer()
