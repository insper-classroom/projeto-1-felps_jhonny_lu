
ambiente = "config_02"
algortimo = "AStar"
agentes = 4


def simulacao(ambiente, algortimo, agentes):
    if ambiente == "config_01" and algortimo == "tradicional" and agentes == 1:
        from traditional_maritime_search.traditional_search_1_agent_1c import main
        main()
    elif ambiente == "config_02" and algortimo == "tradicional" and agentes == 1:
        from traditional_maritime_search.traditional_search_1_agent_2c import main
        main()
    elif ambiente == "config_01" and algortimo == "tradicional" and agentes == 2:
        from traditional_maritime_search.traditional_search_2_agent_1c import main
        main()
    elif ambiente == "config_02" and algortimo == "tradicional" and agentes == 2:
        from traditional_maritime_search.traditional_search_2_agent_2c import main
        main()
    elif ambiente == "config_01" and algortimo == "tradicional" and agentes == 4:
        from traditional_maritime_search.traditional_search_4_agent_1c import main
        main()
    elif ambiente == "config_02" and algortimo == "tradicional" and agentes == 4:
        from traditional_maritime_search.traditional_search_4_agent_2c import main
        main()
    elif ambiente == "config_01" and algortimo == "expanding" and agentes == 1:
        from expanding_square_search.expanding_search_1_agent_1c import main
        main()
    elif ambiente == "config_02" and algortimo == "expanding" and agentes == 1:
        from expanding_square_search.expanding_search_1_agent_2c import main
        main()
    elif ambiente == "config_01" and algortimo == "expanding" and agentes == 2:
        from expanding_square_search.expanding_search_2_agent_1c import main
        main()
    elif ambiente == "config_02" and algortimo == "expanding" and agentes == 2:
        from expanding_square_search.expanding_search_2_agent_2c import main
        main()
    elif ambiente == "config_01" and algortimo == "expanding" and agentes == 4:
        from expanding_square_search.expanding_search_4_agent_1c import main
        main()
    elif ambiente == "config_02" and algortimo == "expanding" and agentes == 4:
        from expanding_square_search.expanding_search_4_agent_2c import main
        main()
    elif ambiente == "config_01" and algortimo == "AStar" and agentes == 1:
        from AStar_search.AStar_search_1_agent_1c import main
        main()
    elif ambiente == "config_02" and algortimo == "AStar" and agentes == 1:
        from AStar_search.AStar_search_1_agent_2c import main
        main()
    elif ambiente == "config_01" and algortimo == "AStar" and agentes == 2:
        from AStar_search.AStar_search_2_agent_1c import main
        main()
    elif ambiente == "config_02" and algortimo == "AStar" and agentes == 2:
        from AStar_search.AStar_search_2_agent_2c import main
        main()
    elif ambiente == "config_01" and algortimo == "AStar" and agentes == 4:
        from AStar_search.AStar_search_4_agent_1c import main
        main()
    elif ambiente == "config_02" and algortimo == "AStar" and agentes == 4:
        from AStar_search.AStar_search_4_agent_2c import main
        main()



simulacao(ambiente, algortimo, agentes)