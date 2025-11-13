import pandas as pd
import numpy as np


def explore_unknown_data(df):
    """探索完全未知的数据集"""

    print("🔍 开始探索未知数据集...")
    print("=" * 60)

    # 1. 最基本信息
    print("📊 数据集基本信息:")
    print(f"   形状: {df.shape} ({df.shape[0]:,} 行 × {df.shape[1]} 列)")
    print(f"   内存使用: {df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB")

    # 2. 快速查看列信息
    print(f"\n📋 数据列信息:")
    print(df.dtypes)

    # 3. 预览数据
    print(f"\n👀 数据预览 (前3行):")
    print(df.head(3))

    # 4. 缺失值快速扫描
    print(f"\n❓ 缺失值扫描:")
    missing_data = df.isnull().sum()
    missing_percent = (missing_data / len(df)) * 100

    missing_report = pd.DataFrame({
        '缺失数量': missing_data,
        '缺失比例%': missing_percent.round(2)
    })

    # 只显示有缺失值的列
    missing_columns = missing_report[missing_report['缺失数量'] > 0]
    if len(missing_columns) > 0:
        print(missing_columns)
    else:
        print("   无缺失值 ✓")

    # 5. 数值列快速统计
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        print(f"\n🔢 数值列快速统计:")
        for col in numeric_cols:
            print(f"   {col}: min={df[col].min()}, max={df[col].max()}, 均值={df[col].mean():.2f}")

    # 6. 文本列快速统计
    text_cols = df.select_dtypes(include=['object']).columns
    if len(text_cols) > 0:
        print(f"\n📝 文本列快速统计:")
        for col in text_cols:
            unique_count = df[col].nunique()
            sample_value = df[col].dropna().iloc[0] if len(df[col].dropna()) > 0 else "无数据"
            print(f"   {col}: {unique_count} 个唯一值, 示例: '{sample_value}'")

    # 7. 自动检测潜在问题
    print(f"\n⚠️  潜在问题检测:")
    issues = []

    # 检测重复行
    duplicate_rows = df.duplicated().sum()
    if duplicate_rows > 0:
        issues.append(f"重复行: {duplicate_rows:,} 条")

    # 检测数值异常
    for col in numeric_cols:
        negative_count = (df[col] < 0).sum()
        if negative_count > 0:
            issues.append(f"{col}有负值: {negative_count:,} 条")

    if issues:
        for issue in issues:
            print(f"   - {issue}")
    else:
        print("   未发现明显问题 ✓")

    return {
        'numeric_columns': list(numeric_cols),
        'text_columns': list(text_cols),
        'missing_columns': list(missing_columns.index) if len(missing_columns) > 0 else []
    }


def interactive_data_investigation(df, insights):
    """基于初步发现的交互式深入探索"""

    print(f"\n🎯 基于发现的深入探索:")
    print("=" * 60)

    # 如果有缺失值，深入探索
    if insights['missing_columns']:
        print(f"\n🔍 缺失值深入分析:")
        for col in insights['missing_columns']:
            missing_count = df[col].isnull().sum()
            print(f"\n   {col} 缺失 {missing_count:,} 条:")

            # 尝试找出缺失值的模式
            if len(insights['numeric_columns']) > 0:
                # 检查缺失值与其他数值列的关系
                numeric_col = insights['numeric_columns'][0]  # 取第一个数值列
                missing_mask = df[col].isnull()
                if missing_mask.sum() > 0:
                    avg_value = df.loc[missing_mask, numeric_col].mean()
                    print(f"     当{col}缺失时，{numeric_col}的平均值: {avg_value:.2f}")


# 主执行流程
if __name__ == "__main__":
    # 1. 读取数据（完全不知道里面有什么）
    file_path = "D:/学习/数据/e_commerce/e_commerce.csv"

    try:
        print(f"📂 正在读取未知数据文件: {file_path}")
        df = pd.read_csv(file_path)
        print("✅ 数据加载成功！开始探索...")

        # 2. 执行探索分析
        insights = explore_unknown_data(df)

        # 3. 基于发现进行深入探索
        interactive_data_investigation(df, insights)

        # 4. 下一步建议
        print(f"\n💡 下一步分析建议:")
        if insights['missing_columns']:
            print("   - 重点分析缺失值的模式和影响")
        if insights['numeric_columns']:
            print("   - 对数值列进行分布分析和异常值检测")
        if insights['text_columns']:
            print("   - 对文本列进行唯一值分析和数据清洗")

    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 {file_path}")
    except Exception as e:
        print(f"❌ 读取文件时出错: {e}")
        print("💡 尝试检查文件格式或编码")