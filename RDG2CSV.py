import xml.etree.ElementTree as ET
import xmltodict
import json
import os

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

def main():
    
    folder_in = "./input/"
    folder_out = "./output/"
    rdg_filepath_in = validate_file("servers.rdg", folder_in)
    csv_filepath_out = build_filepath("servers.ahk", folder_out)
    json_filepath_out = build_filepath("servers.json", folder_out)
    
    mkdir_output(folder_out)
    clear_output_folder([csv_filepath_out, json_filepath_out], folder_out)
    
    rdg_xml = import_xml(rdg_filepath_in)
    rdg_dict = xmltodict.parse(rdg_xml)
    rdg_json = json.dumps(rdg_dict, indent=2)
    export_json(rdg_json, json_filepath_out)
    
    rdg_group_list = rdg_dict['RDCMan']['file']['group']
    output_list = []
    
    # This loop can only parse through 2 nest levels. (ex. Main group > 1st Sub Group > 2nd Sub Group > Server)
    for group in rdg_group_list:
        group_name = group["properties"]["name"]
        if "server" in group.keys():
            for server in group["server"]:
                try:
                    print(server["properties"], group_name)
                except:
                    try:
                        print(group["properties"], group_name)
                    except:                       
                        print(f"Error printing server data from group {group_name}")
        if "group" in group.keys():
            for subgroup in group["group"]:
                subgroup_name = subgroup["properties"]["name"]
                if "server" in subgroup.keys():
                    for server in subgroup["server"]:
                        try:
                            print(server["properties"], group_name, subgroup_name)
                        except:
                            try:
                                print(subgroup["properties"], subgroup_name)
                            except:
                                print(f"Error printing server data from subgroup {subgroup_name}")
                if "group" in subgroup.keys():
                    for subsubgroup in subgroup["group"]:
                        subsubgroup_name = subsubgroup["properties"]["name"]
                        if "server" in subsubgroup.keys():
                            for server in subsubgroup["server"]:
                                try:
                                    print(server["properties"], group_name, subgroup_name, subsubgroup_name)
                                except:
                                    try:
                                        print(subsubgroup["properties"], subsubgroup_name)
                                    except:
                                        print(f"Error printing server data from subsubgroup {subsubgroup_name}")

if __name__ == "__main__":
    main()