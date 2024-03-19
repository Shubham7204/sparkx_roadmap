import json

sys_prompt = """
You are a very smart book author. Make a book index page with all the titles and sub-titles for the book name provided by the user.
Return the output in JSON format.
Example:
{
    "<chapter name>": [
        "<sub topic 1>", 
        "<sub topic 2>"
    ],
    "<chapter name>": [
        "<sub topic 1>", 
        "<sub topic 2>"
    ]
}
"""

def output_sanitizer(prompt):
    begin = prompt.find("{")
    end = prompt.find("}")
    output = prompt[begin: end + 1]
    
    try:
        output = json.loads(output)
    except json.JSONDecodeError:
        return {}
    
    return output

def dict_style_changer(file):
    new = {}
    count = 1

    for k, v in file.items():
        new_key = f"{count}[{k}]"
        count += 1
        temp = []

        for i in v:
            new_value = f"{count}[{i}]"
            count += 1
            temp.append(new_value)
        
        new[new_key] = temp

    return new

def dict_to_mermaid(file):
    file = dict_style_changer(file)
    output = "flowchart TB\n\t"
    arrow = " --> "
    thick_arrow = " ==> "

    for k, v in file.items():
        output += f"subgraph {k}\n\t{arrow.join(v)}\n\tend\n\t"
    
    output += thick_arrow.join(list(file.keys()))

    return output
