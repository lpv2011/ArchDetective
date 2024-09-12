import magic
import subprocess
import sys
import os
import requests

def install_package(package_name):
    os.makedirs(package_name, exist_ok=True)
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--target', package_name, package_name])
        print(f"Package '{package_name}' installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing package '{package_name}': {e}")

def check_wheel_metadata(package_name):
    os_entries = []
    for file_name in os.listdir(package_name):
        if file_name.endswith('.dist-info') and package_name in file_name:
            dist_info_dir = os.path.join(package_name, file_name)
            metadata_file = os.path.join(dist_info_dir, 'METADATA')
            if os.path.isfile(metadata_file):
                try:
                    with open(metadata_file, 'r') as f:
                        for line in f:
                            if line.startswith('Classifier: Operating System'):
                                os_entries.append(line.split(':', 1)[1].strip())
                    if os_entries:
                        print("Metadata includes the following list of OS:")
                        for entry in os_entries:
                            print("-", entry)
                        return os_entries
                except Exception as e:
                    print(f"Error reading '{metadata_file}': {e}")
                return None
    return None

def check_filetype(package_name):
    package_path = os.path.join(package_name, package_name)
    for file_name in os.listdir(package_path):
        if file_name.endswith('.dylib'):
            dylib_file = os.path.join(package_path, file_name)
            try:
                file_type = magic.from_file(dylib_file)
                return file_type
            except Exception as e:
                print(f"Error checking filetype for '{dylib_file}': {e}")
                return None
        elif file_name.endswith('.so'):
            so_file = os.path.join(package_path, file_name)
            try:
                file_type = magic.from_file(so_file)
                return file_type
            except Exception as e:
                print(f"Error checking filetype for '{so_file}': {e}")
                return None
        elif file_name.endswith('.dll'):
            dll_file = os.path.join(package_path, file_name)
            try:
                file_type = magic.from_file(dll_file)
                return file_type
            except Exception as e:
                print(f"Error checking filetype for '{dll_file}': {e}")
                return None
        else:
            print("No OS dependent file found")
            return None
    return None

def pip_wheel_info(package_name):
    url = f"https://pypi.org/simple/{package_name}/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text.lower()
        keywords = ['linux', 'macos', 'win']
        found_keywords = []
        missing_keyword = None

        for keyword in keywords:
            if keyword in html_content:
                found_keywords.append(keyword)
            else:
                missing_keyword = keyword

        if len(found_keywords) == len(keywords):
            return "Found wheels for "+ ','.join(found_keywords)  # Return True and found keywords if all keywords are found
        else:
            return "Missing wheels for "+ ','.join(missing_keyword)  # Return False and missing keyword if any keyword is missing

    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return None, None


if __name__ == "__main__":
    package_name = input("Enter the name of the package to install: ")
    install_package(package_name)

    metadata_file = check_wheel_metadata(package_name)
    if(metadata_file == None):
        print("No OS entries found in metadata")
    else:
        print(metadata_file)

    executable_file  = check_filetype(package_name)
    print(executable_file)

    wheel_check = pip_wheel_info(package_name)
    print(wheel_check)