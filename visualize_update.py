import pandas as pd
import matplotlib.pyplot as plt

# Load the new dataset
df = pd.read_csv("Analysis_Ready_Dataset.csv")

fig, axes = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Updated Study Design: 2-12 Years Age Range\n17 Records (vs 6 with 5-12 years)', 
             fontsize=14, fontweight='bold')

# Age Distribution
ax1 = axes[0, 0]
age_counts = df['Age_Years'].value_counts().sort_index()
ax1.bar(age_counts.index, age_counts.values, color='steelblue', alpha=0.7)
ax1.set_xlabel('Age (years)', fontweight='bold')
ax1.set_ylabel('Count', fontweight='bold')
ax1.set_title('Age Distribution')
ax1.grid(alpha=0.3)
ax1.set_xticks(range(2, 13))

# Age Groups
ax2 = axes[0, 1]
age_group_counts = df['Age_Group'].value_counts()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
ax2.bar(range(len(age_group_counts)), age_group_counts.values, 
        color=colors, alpha=0.7, tick_label=age_group_counts.index)
ax2.set_ylabel('Count', fontweight='bold')
ax2.set_title('Age Group Distribution')
ax2.grid(alpha=0.3, axis='y')
for i, v in enumerate(age_group_counts.values):
    ax2.text(i, v + 0.3, str(v), ha='center', fontweight='bold')

# Outcome Distribution
ax3 = axes[1, 0]
outcome_counts = df['Respiratory_Label'].value_counts()
labels = ['Respiratory\n(1)', 'Non-Respiratory\n(0)']
colors_outcome = ['#FF6B6B', '#95E1D3']
wedges, texts, autotexts = ax3.pie(outcome_counts.values, labels=labels, 
                                     autopct='%1.1f%%', colors=colors_outcome,
                                     startangle=90, textprops={'fontweight': 'bold'})
ax3.set_title('Outcome Distribution\n⚠️ Need more non-respiratory cases!')

# Season Distribution
ax4 = axes[1, 1]
season_counts = df['Season'].value_counts()
season_colors = {'Winter': '#85C1E2', 'Summer': '#FFD93D', 
                 'Monsoon': '#6BCB77', 'Post-Monsoon': '#FAB95B'}
colors_season = [season_colors.get(s, 'gray') for s in season_counts.index]
ax4.bar(range(len(season_counts)), season_counts.values, 
        color=colors_season, alpha=0.7, tick_label=season_counts.index)
ax4.set_ylabel('Count', fontweight='bold')
ax4.set_title('Seasonal Distribution')
ax4.grid(alpha=0.3, axis='y')
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')

plt.tight_layout()
plt.savefig('Study_Design_Update_Summary.png', dpi=300, bbox_inches='tight')
print("✅ Visualization saved: Study_Design_Update_Summary.png")
print("\n📊 Key Findings:")
print(f"   • Sample size: 17 (was 6 with 5-12 years)")
print(f"   • 183% increase in data!")
print(f"   • Most are toddlers (2-4 years): {(df['Age_Group']=='Toddler (2-4)').sum()}")
print(f"   • ⚠️  Class imbalance: 88% respiratory (need more non-respiratory cases)")
print(f"   • Temporal span: {(pd.to_datetime(df['Admission_Date']).max() - pd.to_datetime(df['Admission_Date']).min()).days} days")
