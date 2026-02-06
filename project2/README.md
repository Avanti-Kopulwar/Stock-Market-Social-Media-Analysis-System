
[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ywZhaIZ7)
# Project 2 Report

## Overview
This repository contains the final report and implementation for CS 515 – Social Media Data Science Pipelines (Fall 2025).
Building upon the continuous Reddit and 4chan data-collection system from Project 1, this phase focuses on measuring sentiment, toxicity, and posting activity across both platforms — particularly on 4chan’s /pol/ board.
The project integrates VADER for sentiment scoring and Google Perspective API for toxicity computation.
All required figures, including the /pol/ activity plots for Nov 1–14 (threads/day and posts/hour), were generated and verified for reproducibility on the Binghamton VM

---

## Repository Contents
- data_hunters_project2_report.pdf – Final report in ACM SIGCONF format.
- analyze_sentiment_toxicity_combined.py – Main analysis pipeline integrating VADER and Perspective API.
- generate_dataset_summary_table.py – Retrieves analyzed post statistics and exports LaTeX + image table.
 
- dataset_summary_table.png – Generated summary image of sentiment / toxicity metrics.
- plot_daily_post_counts.py, plot_sentiment_distribution.py, plot_toxicity_distribution.py,
plot_daily_toxicity_trends.py, plot_sentiment_toxicity_scatter.py, plot_top_pol_terms.py,
plot_pol_threads_per_day.py, plot_pol_posts_per_hour.py – Scripts to generate Figures 1–8.

---

# Activate virtual environment
source venv/bin/activate

# Run combined sentiment + toxicity analysis
python3 analyze_sentiment_toxicity_combined.py

# Generate dataset summary table
python3 generate_dataset_summary_table.py

# Produce all required figures
python3 plot_daily_post_counts.py
python3 plot_sentiment_distribution.py
python3 plot_toxicity_distribution.py
python3 plot_daily_toxicity_trends.py
python3 plot_sentiment_toxicity_scatter.py
python3 plot_top_pol_terms.py
python3 plot_pol_threads_per_day.py
python3 plot_pol_posts_per_hour.py
