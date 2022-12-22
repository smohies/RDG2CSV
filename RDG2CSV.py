import xml.etree.ElementTree as ET
import xmltodict
import json
import os
import csv

def validate_file(filename, folder):
    while True:
        filepath = os.path.join(folder, filename)
        if not os.path.isdir(folder):
            os.mkdir(folder)
        if not os.path.isfile(filepath):
            print(f"{filename} not found in ./input/, enter the RDCMan exported XML filename:")
            filename = input()
        else:
            return filepath
        
def build_filepath(filename, folder):
    filepath = os.path.join(folder, filename)
    return filepath

def mkdir_output(folder):
    if not os.path.isdir(folder):
            os.mkdir(folder)
                
def clear_output_folder(filepaths, folder):
    if os.path.isdir(folder):
        for filepath in filepaths:
            if os.path.isfile(filepath):
                print(f"Deleting old file {filepath}")
                os.remove(filepath)
                
def import_xml(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    return ET.tostring(root, encoding='utf-8', method='xml')

def export_json(json, filepath):
    print(f"Exporting {filepath}")
    with open(filepath, "w") as json_file:
        json_file.write(json)
        
def pull_server_properties(server, group, group_name, subgroup_name=""):
    properties = {}
    logon = {"userName": "", "domain": ""}
    try:
        properties = server["properties"]
    except:
        properties = group["properties"]
    properties["group"] = group_name
    properties["subgroup"] = subgroup_name
    try:
        logon["userName"] = server["logonCredentials"]["userName"]
        logon["domain"] = server["logonCredentials"]["domain"]
    except:
        try:
            logon["userName"] = group["logonCredentials"]["userName"]
            logon["domain"] = group["logonCredentials"]["domain"]
        except:
            pass
    properties["userName"] = logon["userName"]
    properties["domain"] = logon["domain"]
    return properties

def standarize_properties(property_list):
    std_property_list = []
    for property in property_list:
        std_property = {"displayName":"", "name":"", "group":"", "subgroup":"", "userName":"", "domain":""}
        for key in std_property.keys():      
            if key in property.keys():
                std_property[key] = property[key]
        std_property_list.append(std_property)
    return std_property_list

def export_csv(filepath, headers, dicitonary_list):
    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=',', quotechar='"', lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(dicitonary_list)

def main():
    
    folder_in = "./input/"
    folder_out = "./output/"
    rdg_filepath_in = validate_file("servers.rdg", folder_in)
    csv_filepath_out = build_filepath("servers.csv", folder_out)
    json_filepath_out = build_filepath("servers.json", folder_out)
    
    mkdir_output(folder_out)
    clear_output_folder([csv_filepath_out, json_filepath_out], folder_out)
    
    rdg_xml = import_xml(rdg_filepath_in)
    rdg_dict = xmltodict.parse(rdg_xml)
    rdg_json = json.dumps(rdg_dict, indent=2)
    export_json(rdg_json, json_filepath_out)
    
    rdg_group_list = rdg_dict['RDCMan']['file']['group']
    output_header = ["displayName", "name", "group", "subgroup", "userName", "domain"]
    output_list = []
    
    # This loop will only traverse for a single sub-level (sub-group)
    for group in rdg_group_list:
        group_name = group["properties"]["name"]
        if "server" in group.keys():
            for server in group["server"]:
                output_list.append(pull_server_properties(server, group, group_name))
        if "group" in group.keys():
            for subgroup in group["group"]:
                subgroup_name = subgroup["properties"]["name"]
                if "server" in subgroup.keys():
                    for server in subgroup["server"]:
                        output_list.append(pull_server_properties(server, subgroup, group_name, subgroup_name))
                                
    output_list = standarize_properties(output_list)
    export_csv(csv_filepath_out, output_header, output_list)
        
if __name__ == "__main__":
    main()