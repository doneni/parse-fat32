import sys

file_path = "parse-fat\\fat32.dd"

with open(file_path, 'rb') as f:
    data = f.read()

def hex2str(hex_value):
        return bytes.fromhex(hex_value).decode('utf-8')

def parse_boot_record():
    # FAT32 Boot Record
    br_offset = 0
    bytes_per_sector = int.from_bytes(data[br_offset + 11 : br_offset + 13], byteorder='little')
    reserved_sector_count = int.from_bytes(data[br_offset + 14 : br_offset + 16], byteorder='little')
    fat_size = int.from_bytes(data[br_offset + 36 : br_offset + 41], byteorder='little')

    return {
        'bytes_per_sector': bytes_per_sector,
        'reserved_sector_count': reserved_sector_count,
        'fat_size': fat_size,
    }

def parse_fat_table(fat_offset, target_cluster):
    # Parse FAT table 
    cluster_chain = []
    i = target_cluster
    start_offset = fat_offset + 4 * i
    end_offset = fat_offset + 4 * (i + 1)
    while(1):
        cluster_chain.append(i)
        if(data[start_offset : end_offset] == b'\xff\xff\xff\x0f'):
            print("[+] Caught 'xffffff0f' at", start_offset)
            break
        else:
            i = i + 1
            start_offset = start_offset + 4
            end_offset = end_offset + 4
    return cluster_chain

def check_integrity(fat_offset, target_cluster, cluster_chain):
    # Check integiry by parsing second FAT table
    if (cluster_chain == parse_fat_table(fat_offset, target_cluster)):
        print("[+] Integrity Check Passed")
        return(cluster_chain)
    else:
        print("[-] Integrity Check Returned with Error: First FAT table and second FAT table doesn't match. Could be index out of range")
        return None

def main():
    if len(sys.argv) < 2:
        print("[-] Usage: Python3 <file_name> <target_cluster>")
        print("[-] Example: Python3 work3.py 100")
        exit()
    else:
        print("[+] Parsing FAT32 Format")
        print("[*] File Path:", file_path)
        target_cluster = int(sys.argv[1])
        print("[*] Target Cluster:", target_cluster)

    print("\n[+] Parsing Boot Record")
    br_info = parse_boot_record()
    print("[*] br_info:", br_info)
    
    # addr calculation
    addr_fat_table = []
    addr_fat_table.append(br_info['reserved_sector_count'] * br_info['bytes_per_sector'])
    addr_fat_table.append((br_info['reserved_sector_count'] + br_info['fat_size']) * br_info['bytes_per_sector'])
    print("[*] FAT Tables are At:", addr_fat_table)

    print("\n[+] Parsing First FAT Table at", addr_fat_table[0])
    cluster_chain = parse_fat_table(addr_fat_table[0], target_cluster)
    print("[+] First FAT Table Parsing Done")
    print("\n[+] Checking Integrity by Parsing Second FAT Table at", addr_fat_table[1])
    if (check_integrity(addr_fat_table[1], target_cluster, cluster_chain)):
        print("[*] Cluster Chain:", cluster_chain)

if __name__ == "__main__":
    main()