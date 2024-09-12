import apt
import magic
import subprocess
import requests
import mimetypes

def architecture_scan(package_name):
    cache = apt.cache.Cache()
    cache.open()

    if package_name not in cache:
        print(f"Package is not found in the cache.")
        return

    package = cache[package_name]
    
    arch = package.architecture()
    print(f"Package Architecture: "+ arch)
    
    output = subprocess.run(['apt-cache', 'show', package_name], capture_output = True, text = True)
    
    multi_search_str = 'Multi-Arch:'
    multiarch_output = subprocess.run(['grep', multi_search_str], input = output.stdout, capture_output = True, text = True)
    if (multiarch_output == 'foreign'):
        print(f"Package is cross-compiling.")
    else:
        print(f"Package is not cross-compiling.")
    
    filename_search_str = 'Filename: '
    filename_output = subprocess.run(['grep', filename_search_str], input = output.stdout, capture_output = True, text = True)
    print('Package download link: ' + filename_output.stdout.strip())
    


if __name__ == "__main__":
    package_name = input("Enter package: ")
    architecture_scan(package_name)
