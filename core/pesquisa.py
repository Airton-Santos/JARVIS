from ddgs import DDGS
from deep_translator import GoogleTranslator

def pesquisar_resumido(termo):
    """
    Pesquisa no DuckDuckGo e retorna:
    - resumo traduzido para português se necessário
    - link da fonte principal
    - outros links
    """
    resultados = []
    with DDGS() as ddgs:
        for r in ddgs.text(termo, max_results=5):
            title = r.get("title", "Sem título")
            href = r.get("href", "")
            body = r.get("body", "")
            resultados.append({"title": title, "href": href, "body": body})

    if not resultados:
        return {"resumo": "Nenhum resultado encontrado.", "fonte": None, "outros_links": []}

    resumo = resultados[0]["body"] or resultados[0]["title"]
    
    # traduz para português
    resumo_pt = GoogleTranslator(source='auto', target='pt').translate(resumo)

    fonte = resultados[0]["href"]
    outros_links = [r["href"] for r in resultados[1:]]

    return {"resumo": resumo_pt, "fonte": fonte, "outros_links": outros_links}
