from langgraph_flow import bootstrap

agent = bootstrap()
query = "Please summarize `data/sample_contract.pdf`. List parties, key obligations, important dates, any indemnities, and recommended next steps."
res = agent.invoke({"messages": [{"role": "user", "content": query}]})
print(res)
