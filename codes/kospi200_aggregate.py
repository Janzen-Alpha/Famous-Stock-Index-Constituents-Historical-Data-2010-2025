"""
聚合 KOSPI200 历年成分股数据
从各年 CSV 文件中提取股票代码，生成"年份-成分股"对照表
第一行是年份，每列是该年的成分股代码列表

年份映射规则：文件名 YYYYMMDD → 次年即为该成分股的有效年份
例如：20091230.csv → 2010年的成分股
"""

import csv
import os
import re
from pathlib import Path

# 工作目录
DATA_DIR = Path(__file__).parent

def parse_year_from_filename(filename: str) -> int:
    """从文件名解析年份，YYYYMMDD.csv → 次年"""
    match = re.match(r"(\d{4})\d{4}\.csv", filename)
    if not match:
        raise ValueError(f"无法解析文件名: {filename}")
    file_year = int(match.group(1))
    return file_year + 1  # 成分股在次年生效


def read_codes_from_csv(filepath: Path) -> list[str]:
    """从 CSV 文件中提取所有股票代码（Issue code 列）"""
    codes = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row.get("Issue code", "").strip()
            if code:
                # 去除可能的引号和空格
                code = code.strip('"').strip("'").strip()
                if code.isdigit():
                    codes.append(code)
    return codes


def main():
    # 收集所有 CSV 文件
    csv_files = sorted(DATA_DIR.glob("*.csv"))
    # 过滤掉输出文件（如果存在）
    csv_files = [f for f in csv_files if not f.name.startswith("kospi200_") and f.name != "output.csv"]

    if not csv_files:
        print("未找到 CSV 文件！")
        return

    print(f"找到 {len(csv_files)} 个 CSV 文件：")
    
    # 存储每年的成分股
    year_codes: dict[int, list[str]] = {}
    
    for csv_file in csv_files:
        year = parse_year_from_filename(csv_file.name)
        codes = read_codes_from_csv(csv_file)
        year_codes[year] = codes
        print(f"  {csv_file.name} → {year}年: {len(codes)}只成分股")

    # 按年份排序
    sorted_years = sorted(year_codes.keys())
    
    # =============================================
    # 输出1：宽表 —— 年份为列，行为序号（对齐模式）
    # =============================================
    # 每列的行数取最大值
    max_count = max(len(codes) for codes in year_codes.values())
    
    output1_path = DATA_DIR / "kospi200_constituents_wide.csv"
    with open(output1_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        # 表头：年份
        writer.writerow(sorted_years)
        # 数据行
        for i in range(max_count):
            row = []
            for year in sorted_years:
                codes = year_codes[year]
                row.append(codes[i] if i < len(codes) else "")
            writer.writerow(row)
    print(f"\n宽表已保存: {output1_path} ({max_count}行 × {len(sorted_years)}列)")

    # =============================================
    # 输出2：长表 —— 年份 + 成分股列表（每行一只）
    # =============================================
    output2_path = DATA_DIR / "kospi200_constituents_long.csv"
    with open(output2_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Code"])
        for year in sorted_years:
            for code in year_codes[year]:
                writer.writerow([year, code])
    print(f"长表已保存: {output2_path}")

    # =============================================
    # 输出3：去重全部代码 —— 方便用 pykrx 批量下载
    # =============================================
    all_codes = set()
    for codes in year_codes.values():
        all_codes.update(codes)
    
    output3_path = DATA_DIR / "kospi200_all_codes.txt"
    with open(output3_path, "w", encoding="utf-8") as f:
        for code in sorted(all_codes):
            f.write(code + "\n")
    print(f"去重全部代码已保存: {output3_path} (共 {len(all_codes)} 只)")

    # =============================================
    # 统计摘要
    # =============================================
    print("\n" + "=" * 60)
    print("历年成分股统计摘要")
    print("=" * 60)
    print(f"{'年份':<8} {'数量':<8} {'示例前5只'}")
    print("-" * 60)
    for year in sorted_years:
        codes = year_codes[year]
        preview = ", ".join(codes[:5])
        print(f"{year:<8} {len(codes):<8} {preview}")
    
    # 新增/退出统计
    print("\n" + "=" * 60)
    print("成分股变动分析")
    print("=" * 60)
    for i in range(1, len(sorted_years)):
        prev_year = sorted_years[i - 1]
        curr_year = sorted_years[i]
        prev_set = set(year_codes[prev_year])
        curr_set = set(year_codes[curr_year])
        new_entries = curr_set - prev_set
        removed = prev_set - curr_set
        print(f"\n{prev_year} → {curr_year}:")
        print(f"  新增 {len(new_entries)}: {', '.join(sorted(new_entries)) if new_entries else '无'}")
        print(f"  退出 {len(removed)}: {', '.join(sorted(removed)) if removed else '无'}")

    print("\n完成！")


if __name__ == "__main__":
    main()
