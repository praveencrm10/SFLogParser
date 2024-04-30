import os

keywords = {
    "start":{
        "cd_unit":"CODE_UNIT_STARTED",
        "exe":"EXECUTION_STARTED",
        "prof":"CUMULATIVE_PROFILING_BEGIN",
        "method":"METHOD_ENTRY",
        "constructor":"CONSTRUCTOR_ENTRY"
    },
    "end":{
        "cd_unit":"CODE_UNIT_FINISHED",
        "exe":"EXECUTION_FINISHED",
        "prof":"CUMULATIVE_PROFILING_END",
        "method":"METHOD_EXIT",
        "constructor":"CONSTRUCTOR_EXIT"
    }
}

html_escape_chars = {
    "<": "&lt;",
    ">": "&gt;",
    #"&": "&amp;",
    "\"": "&quot;",
    "'": "&#39;",
    "`": "&#96;",
    "/": "&#47;"
    # Add more HTML escape characters as needed
}

html_init = '<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="styles.css">'
html_end = '<script src="script.js"></script></body></html>'
table = {
    "heap":False,
    "variable_assign":False
}
# This function is used to write the html content
def write_file(folder_path,filename,file_content):
    with open(os.path.join(folder_path,filename),'w') as file:
        file.write('\n'.join(file_content))

# Open log file from specified folder
def open_file(folder_path,filename):
    file_content = ""
    full_file_path = os.path.join(folder_path,filename)
    with open(full_file_path,'r') as file:
        file_content = file.read()
    return file_content

# Convert String to list of lines
def get_lines(file_content):
    if file_content is not None:
        all_lines = file_content.split("\n")
        return all_lines
    return None

# Find presence of string in the text
def find_str(string_to_find,content):
    if content is not None and string_to_find in content:
        return True
    return False

# Find the method Name from the string
def extract_method_name(line):
    if line is not None:
        parts = line.split("|")
        if len(parts) > 0:
            return parts[len(parts)-1]
    return None

def html_escape(text):
    for char,escape_char in html_escape_chars.items():
        text = text.replace(char,escape_char)
    return text

def is_start(line):
    starts = keywords["start"]
    for key,val in starts.items():
        if val in line:
            return True
    else:
        return False
    
def is_end(line):
    starts = keywords["end"]
    for key,val in starts.items():
        if val in line:
            return True
    else:
        return False

def variable_assignment_handler(line):
    if find_str("VARIABLE_ASSIGNMENT",line):
        parts = line.split("|")
        timestamp = parts[0]
        lineno = parts[2]
        variable_name = parts[3]
        variable_value = parts[4]
        if table["variable_assign"]:
            return '<tr>'+'<td>'+timestamp+'</td>' + '<td>'+lineno+'</td>' + '<td>'+variable_name+'</td>' + '<td>'+variable_value+'</td>' + '</tr>'
        else:
            table["variable_assign"] = True
            first_line = '<table><thead><th>'+'<td>Timestamp<td>' + '<td>Line No<td>'+ '<td>Variable Name<td>'+'<td>Value<td>' + '</th></thead>'
            line = first_line + variable_assignment_handler(line) + "<tbody>"
    else:
        if table["variable_assign"]:
            table["variable_assign"] = False
            line = line + "</tbody></table>"
    return line

def is_heap_allocations(line):
    return True if "HEAP_ALLOCATE" in line else False

def create_html_line(line):
    line = html_escape(line)
    if is_start(line):
        return '<button class="accordion">'+extract_method_name(line)+'</button><div class="panel"><br/>'+line+'<br/>'
    elif is_end(line):
        return line +"<br/></div>"
    elif is_heap_allocations(line):
        return ''
    line = variable_assignment_handler(line)
    return line+"<br/>"

def create_html_wrapper(all_lines):
    new_lines = []
    new_lines.append(html_init)
    for line in all_lines:
        new_lines.append(create_html_line(line))
    new_lines.append(html_end)
    return new_lines

if __name__ == "__main__":
    folder_path = "C:\\Users\\Praveen\\Downloads\\"
    filename = "apex-07L5i00000HIwS7EAL"

    input_file_name = filename + '.log'
    output_file_name = filename + '.html'

    output_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'templates')
    print(output_folder_path)

    file_content = open_file(folder_path,input_file_name)
    all_lines = get_lines(file_content)
    new_lines = create_html_wrapper(all_lines)
    if len(new_lines) > 0:
        print(len(new_lines))
    write_file(output_folder_path,output_file_name,new_lines)
    print(output_folder_path+output_file_name)