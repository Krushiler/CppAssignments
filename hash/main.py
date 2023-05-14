import os
import time

def crc_hash(key: str) -> int:
    h = 0
    for char in key:
        h = (h << 5) ^ (h >> 27) ^ ord(char)
    return h

def pjw_hash(key: str) -> int:
    h = 0
    for char in key:
        h = (h << 4) + ord(char)
        g = h & 0xf0000000
        if g != 0:
            h = h ^ (g >> 24) ^ g
    return h

def buz_hash(key: str) -> int:
    R = lambda c: ord(c) % 256
    h = 0
    for char in key:
        highorder = h & 0x80000000
        h = (h << 1) ^ (highorder >> 31) ^ R(char)
    return h

def find_duplicates(files: list[str], hash_function: callable) -> list[str]:
    duplicates = []
    hash_counts = {}
    
    for file in files:
        if os.path.isfile(file):
            with open(file, 'r') as f:
                data = f.read()
                file_hash = hash_function(data)
                
                if file_hash in hash_counts:
                    duplicates.append(file)
                    hash_counts[file_hash] += 1
                else:
                    hash_counts[file_hash] = 1
    
    return duplicates

if __name__ == '__main__':
    files = ['files/' + file for file in os.listdir('files')]
    
    hash_functions = {
        'CRC': crc_hash,
        'PJW': pjw_hash,
        'BUZ': buz_hash,
        'Built-in': hash
    }
    
    for name, hash_function in hash_functions.items():
        start_time = time.time()
        duplicates = find_duplicates(files, hash_function)
        end_time = time.time()
        duration = end_time - start_time
        
        print(f'Hash Function: {name}')
        print(f'Number of Duplicates: {len(duplicates)}')
        print(f'Time: {duration} seconds')
        print('---')
