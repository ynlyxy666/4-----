from tqdm import tqdm

def compute_pi_hex_digit(n):
    """使用BBP算法计算π的第n位十六进制小数（索引从1开始）"""
    n -= 1  # 算法索引从0开始
    total = 0.0
    
    # 四个求和项的系数和分母配置
    configs = [
        (4, 1),
        (-2, 4),
        (-1, 5),
        (-1, 6)
    ]
    
    with tqdm(total=4, desc="整体进度") as pbar:
        results = []
        for coeff, denom in configs:
            series_sum = 0.0
            # 主项计算部分
            for k in tqdm(range(n+1), desc=f"计算8k+{denom}", leave=False):
                denominator = 8*k + denom
                exponent = n - k
                numerator = pow(16, exponent, denominator)
                series_sum = (series_sum + numerator/denominator) % 1.0
            
            # 尾项计算部分
            k = n + 1
            while True:
                denominator = 8*k + denom
                term = pow(16, n - k) / denominator
                if term < 1e-15: 
                    break
                series_sum = (series_sum + term) % 1.0
                k += 1
                
            results.append(coeff * series_sum)
            pbar.update(1)
    
    # 合并结果并获取十六进制位
    final = sum(results) % 1.0
    return int(final * 16) % 16

if __name__ == "__main__":
    target_position = 114514
    hex_digit = compute_pi_hex_digit(target_position)
    print(f"π的第{target_position}位十六进制数字是：{hex(hex_digit)[2:]}")


# This is just for demonstration - NOT ACTUALLY EXECUTABLE IN PRACTICE
from decimal import Decimal, getcontext

def compute_pi_decimal(n):
    getcontext().prec = n + 10  # Set precision
    pi = Decimal(0)
    C = 426880 * Decimal(10005).sqrt()
    
    # Chudnovsky algorithm
    for k in range(n//15 + 2):  # Very simplified iteration control
        numerator = (-1)**k * Decimal(13591409 + 545140134*k)
        denominator = Decimal(3)**(3*k) * (Decimal(math.factorial(k))**3) * Decimal(640320)**(3*k + 1.5)
        pi += numerator / denominator
    
    return C * pi

# This would require HPC-level resources to calculate N=114514