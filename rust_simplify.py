import subprocess

def run_moves_through_rust(moves):
    # 1. Write moves to src/input.txt
    with open("src/input.txt", "w") as f:
        f.write(" ".join(str(m) for m in moves))

    # 2. Run `cargo r`
    subprocess.run(["cargo", "r", "--release"], check=True)

    # 3. Read and parse output
    with open("src/output.txt") as f:
        data = f.read().replace(',', '').replace('[', '').replace(']', '').split()
    
    o = []
    for tok in data:
        try:
            o.append(int(tok))
        except:
            o.append((int(tok[1:-1]),))


    return o