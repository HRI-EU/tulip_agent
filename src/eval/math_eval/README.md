# math_eval

# Instructions
1. Specify settings in `math_eval_settings.yaml`
   * Agent ablations to include
   * Tools module to be used
   * Language model to be used
   * File with tasks and ground truth
   * Optionally specify a subset of tasks to be executed as a list via the `task_filter` - will run all tasks if set to `null`
2. Run the evaluation with `python math_eval.py`
3. Analyze results and plot with `python log_analysis.py`; uses the most recent log file unless one is specified in `math_eval_settings.yaml`

## Results
![math eval plot](../../../docs/static/images/math.eval.png)
```yaml
# Settings
number_of_runs: 5
tools: math_tools
model: "gpt-3.5-turbo-0125"
embedding_model: "text-embedding-3-large"
tulip_top_k: 5
search_similarity_threshold: null
```

Note: To avoid a bias towards the tulip architecture, the costs for creating the tool library
are currently added to the embeddings costs of **every single** query, even though it could be reused
