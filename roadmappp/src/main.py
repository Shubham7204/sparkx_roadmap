import streamlit as st
import openai
import streamlit.components.v1 as components
import base64

from roadmapgpt import ai
from roadmapgpt.utils import output_sanitizer, dict_to_mermaid

api_key = "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"  # Your OpenAI key

def mermaid(code):
    chart_height = max(600, len(code.split('\n')) * 20)
    chart_id = 'mermaid-chart'
    components.html(
        f"""
        <style>
        #{chart_id} {{
            overflow: auto;
            max-height: 600px;
        }}
        </style>
        <div id="{chart_id}">
        <pre class="mermaid">
            {code}
        </pre>
        </div>
        <button onclick="downloadChart()">Download Chart</button>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true }});
            
            function downloadChart() {{
                var svgContent = document.querySelector('.mermaid svg');
                var serializer = new XMLSerializer();
                var svgString = serializer.serializeToString(svgContent);
                var blob = new Blob([svgString], {{type: "image/svg+xml"}});
                var url = URL.createObjectURL(blob);
                var link = document.createElement("a");
                link.href = url;
                link.download = "chart.svg";
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }}
        </script>
        """,
        width=800, height=chart_height
    )

def display(user_prompt, content):
    output = content.choices[0].message['content']
    output = output_sanitizer(output)

    if output == {}:
        st.write("Output Parsing Error. Try again with a similar sounding prompt.")
    else:
        output = dict_to_mermaid(output)
        mermaid(output)

st.sidebar.markdown("# RoadmapGPT 🗺️")
user_prompt = st.sidebar.text_input("Enter a domain to generate roadmap", "")

if st.sidebar.button("Generate Roadmap") and user_prompt.strip():
    llm_output = ai.getOutput(user_prompt, api_key)
    display(user_prompt, llm_output)

st.sidebar.markdown("---")
st.sidebar.markdown("Team Hack Hustlers")
