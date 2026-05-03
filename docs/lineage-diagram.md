\# Lineage Diagram: IDS568 Final Project RAG System



```text

SOURCE DOCUMENTS

&#x20; rag\_basics.txt

&#x20; chunking.txt

&#x20; embeddings.txt

&#x20; vector\_databases.txt

&#x20; grounding\_evaluation.txt

&#x20;       |

&#x20;       v

DOCUMENT LOADING

&#x20; load\_documents()

&#x20;       |

&#x20;       v

CHUNKING

&#x20; chunk\_size = 500

&#x20; chunk\_overlap = 50

&#x20; total\_chunks = 14

&#x20;       |

&#x20;       v

EMBEDDING

&#x20; sentence-transformers/all-MiniLM-L6-v2

&#x20; embedding\_dimension = 384

&#x20;       |

&#x20;       v

VECTOR INDEX

&#x20; FAISS IndexFlatL2

&#x20; index\_size = 14 vectors

&#x20;       |

&#x20;       v

RETRIEVAL

&#x20; default top-k = 3

&#x20; A/B test treatment top-k = 5

&#x20;       |

&#x20;       v

PROMPT CONSTRUCTION

&#x20; query + retrieved chunks + system instruction

&#x20;       |

&#x20;       v

GENERATION

&#x20; mistral:7b-instruct through local Ollama

&#x20;       |

&#x20;       v

FASTAPI SERVICE

&#x20; /health

&#x20; /ask

&#x20; /metrics

&#x20;       |

&#x20;       v

MONITORING

&#x20; Prometheus metrics

&#x20; Grafana dashboard JSON

&#x20;       |

&#x20;       v

GOVERNANCE

&#x20; system card

&#x20; audit trail

&#x20; risk register

&#x20; drift diagnostic report

