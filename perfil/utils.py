def calcula_total(obj, campo):
    total = 0
    for i in obj:
        total += getattr(i, campo)

    return total
def formata_float(obj):
    return f"{obj:_.2f}".replace('.',',').replace('_','.')