# parse-fat32

parsing FAT32 format image file

1. parsing boot record && getting some properties
2. parsing first FAT table
3. checking integrity by parsing second FAT table
4. printing cluster chain that comes after targer cluster

Usage:
<pre>
  <code>
    Python3 parse-fat32.py /<target_cluster/>
  </code>
</pre>

Example:
<pre>
  <code>
    Python3 parse-fat32.py 100
  </code>
</pre>
