import os
for fname in os.listdir("."):
    orig_name = fname[:-3]
    base_name = orig_name[:-3]
    if "_v0" in fname:
        ext = 1
    elif "_v1" in fname:
        ext = 2
    else:
        continue
    new_name = f"{base_name}_v{ext}"
    new_fname = new_name+".py"
    for i in range(ext):
        print(f'{base_name}_v{i} = DepreciatedModule("{base_name}", "v{i}", "v{ext}")')
    os.rename(fname, new_fname)
