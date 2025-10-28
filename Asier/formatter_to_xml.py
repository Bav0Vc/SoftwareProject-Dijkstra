import xml.etree.ElementTree as ET
import os

"""
The primary function, `format_to_xml`, processes an array of triples, where each triple contains three elements:
1. The desired list of variables name (as a string).
2. The desired single variable name (as a string).
3. A string representing the variable values in a format compatible with the Jack3 website. 
   This format typically consists of a Python-style `list` with values enclosed in quotes, e.g., 
   - `list('[2, 4, 8, 12, 14, 15, 16, 17, 19]', '[1, 2, 4, 5, 8, 15, 16, 17, 19]', ...)`
   - or `list('2', '16', '13', '11', '9')`.

Additionally, the function requires the path to a folder where an XML file will be located. 
The folder is expected to contain exactly one XML file, which will be processed. 
The provided variable names and their corresponding values will be appended to the XML, 
ensuring the variables are added in the appropriate format.

**Use Case Example:**
1. Prepare an array of variable declarations, each with a name, single_name and a string formatted in the Jack3 paste format.
2. Call `format_to_xml(folder_path, name_input_array)` where `folder_path` is the path to the folder containing the XML file 
   and `name_input_array` is the array of tuples.
3. The XML will be modified with the new variables and saved back to the same file.
"""

def format_single_input_to_xml(name, input_str, current_id):
    """
    Formats a single input string into an XML VariableDeclaration block.
    """
    xml_output = f"""
<VariableDeclaration id="{current_id + 1}">
  <name>{name}</name>
  <initializationCode id="{current_id + 2}">
    <code>{input_str}</code>
    <domain>MATH</domain>
  </initializationCode>
</VariableDeclaration>
"""
    return xml_output, current_id + 2

def generate_variable_declarations_from_array(start_id, name_input_array, question_number, question_amount, exercise_constants: list[str, str]|None=None):
    """
    Generates a list of VariableDeclaration XML strings from the given input array.
    """
    declarations = []
    current_id = start_id

    current_id = current_id + 1

    index_name = 'index_question_' + str(question_number)
    input = f"randomIntegerBetween(0, {question_amount})"
    xml_output, current_id = format_single_input_to_xml(index_name, input, current_id)
    declarations.append(xml_output)
    
    for name, single_name, input_str in name_input_array:
        # generate and append the variables
        xml_output, current_id = format_single_input_to_xml(name, input_str, current_id)
        declarations.append(xml_output)

        # generate and append the variable for a single task
        input = f"getFromList([var={index_name}],[var={name}])"
        xml_output, current_id = format_single_input_to_xml(single_name, input, current_id)
        declarations.append(xml_output)
        
    if exercise_constants is not None:
        for exercise_constant in exercise_constants:
            constant_name, constant_value = exercise_constant
            xml_output, current_id = format_single_input_to_xml(constant_name, constant_value, current_id)
            declarations.append(xml_output)
    
    return declarations

def append_declarations_to_xml(root, variable_declarations, new_declarations):
    """
    Appends new VariableDeclaration XML elements to the variableDeclarations node.
    """
    for decl in new_declarations:
        decl_element = ET.fromstring(decl)
        variable_declarations.append(decl_element)

def fix_ids_in_xml_tree(root, start_id):
    """
    Adjusts all IDs in the XML tree to ensure sequential order starting from `start_id`.
    """
    max_id = start_id - 1
    for elem in root.iter():
        if 'id' in elem.attrib:
            elem_id = int(elem.attrib['id'])
            if elem_id >= start_id:
                elem.attrib['id'] = str(max_id + 1)
                max_id += 1

def process_xml(xml_path, name_input_array, question_number, question_amount, exercise_constants: list[str, str]|None=None):
    """
    Processes the XML file at `xml_path` by applying the transformations.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    variable_declarations = root.find('.//variableDeclarations')
    current_id = int(variable_declarations.attrib['id'])

    new_declarations = generate_variable_declarations_from_array(current_id, name_input_array, question_number, question_amount, exercise_constants)

    append_declarations_to_xml(root, variable_declarations, new_declarations)

    fix_ids_in_xml_tree(root, current_id)

    xml_str = ET.tostring(root, encoding='unicode', method='xml')

    # Ensure that all single quotes are replaced by &apos;
    xml_str = xml_str.replace("'", "&apos;")

    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)

def find_xml_path(folder_path):
    xml_files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
    if len(xml_files) != 1:
        raise ValueError("The folder must contain exactly one .xml file.")

    return os.path.join(folder_path, xml_files[0])

def clear_variable_declarations(folder_path):
    """
    Clears all contents within the <variableDeclarations> tag of an XML file.

    This function performs the following steps:
    - Locates the XML file in the specified folder (the folder must contain exactly one XML file).
    - Removes all child elements within the <variableDeclarations> tag.
    - Saves the updated XML content back to the original file.

    Parameters:
    - folder_path (str): Path to the folder containing the XML file.
    """

    xml_path = find_xml_path(folder_path)

    tree = ET.parse(xml_path)
    root = tree.getroot()

    variable_declarations = root.find('.//variableDeclarations')
    if variable_declarations is not None:
        for child in list(variable_declarations):
            variable_declarations.remove(child)

        xml_str = ET.tostring(root, encoding='unicode', method='xml')

        xml_str = xml_str.replace("'", "&apos;")

        with open(xml_path, 'w', encoding='utf-8') as f:
            f.write(xml_str)
    else:
        raise ValueError("<variableDeclarations> tag not found in the XML file.")

def format_to_xml(folder_path, name_input_array, question_number, question_amount, exercise_constants: list[str, str]|None=None):
    """
    Processes the XML file in a specified folder and appends variable declarations in a Jack3-compatible format.

    This function performs the following steps:
    - Locates the XML file in the specified folder (the folder must contain exactly one XML file).
    - Appends new variable declarations to the XML based on the provided input array.
    - Ensures sequential ID assignment across all XML elements.
    - Saves the updated XML content back to the original file.

    Parameters:
    - folder_path (str): Path to the folder containing the XML file.
    - name_input_array (list[tuple]): A list of tuples `(variable_name, single_name, values_string)` representing:
        - variable_name: The name of the variable list.
        - single_name: The name of the single-task variable.
        - values_string: A string representing values in Jack3-compatible format (e.g., Python-style lists or values).
    - question_number (int): The index of the current question for variable naming.
    - question_amount (int): The total number of questions for index range generation.
    - exercise_constants (list[str, str] | None): A list of tuples `(constant_name, constant_value)` representing:
        - constant_name: The label of the constant to be added exercise-wide. This constant applies to the entire exercise.
        - constant_value: Value of the constant. Can also be an equation.

    Returns:
    None
    """

    xml_path = find_xml_path(folder_path)

    process_xml(xml_path, name_input_array, question_number, question_amount, exercise_constants)
