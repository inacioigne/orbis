from urllib.parse import urlparse

from lib.parser.deep_get import deep_get
from lib.parser.license import first_license_url

OPEN_LICENSE_PATTERNS = [
    "creativecommons.org/licenses/",
    "creativecommons.org/publicdomain/",
    "cc-by",
    "cc by",
    "cc-by-sa",
    "cc by-sa",
    "cc-by-nc",
    "cc by-nc",
    "cc0",
]

TEXT_MINING_LICENSE_PATTERNS = [
    "elsevier.com/tdm/userlicense",
    "text and data mining",
    "tdm",
]

def is_tdm_license(url: str | None) -> bool:
    if not url:
        return False
    u = url.lower().strip()
    return any(pattern in u for pattern in TEXT_MINING_LICENSE_PATTERNS)

def is_open_license(url: str | None) -> bool:
    if not url:
        return False
    u = url.lower().strip()
    return any(pattern in u for pattern in OPEN_LICENSE_PATTERNS)

def extract_license_start_date(licenses):
    """
    Tenta extrair a data de início da licença, se vier no formato Crossref:
    [{"start": {"date-parts": [[2026, 1, 1]]}, "URL": "..."}]
    """
    if not isinstance(licenses, list):
        return None

    for item in licenses:
        if not isinstance(item, dict):
            continue
        start = item.get("start")
        if not isinstance(start, dict):
            continue
        parts = start.get("date-parts")
        if parts and parts[0]:
            p = parts[0]
            year = p[0]
            month = p[1] if len(p) > 1 else 1
            day = p[2] if len(p) > 2 else 1
            return f"{year:04d}-{month:02d}-{day:02d}"
    return None

def _link_says_free(link_item: dict) -> bool | None:
    """
    Interpreta sinais de acesso em message['link'].
    Retorna:
      True  -> há evidência de acesso livre
      False -> há evidência de acesso restrito
      None  -> inconclusivo
    """
    if not isinstance(link_item, dict):
        return None

    text = " ".join(
        str(link_item.get(k, "")).strip().lower()
        for k in ["content-version", "content-type", "intended-application"]
    )

    # Alguns registros Crossref trazem algo como:
    # "intended-application": "text-mining"
    if "text-mining" in text or "tdm" in text:
        return False

    # Alguns publishers indicam explicitamente livre acesso
    for key in ["URL", "url"]:
        value = str(link_item.get(key, "")).lower()
        if any(term in value for term in ["openaccess", "open-access", "oa=true", "free"]):
            return True

    return None


def build_conditions_of_access(data: dict) -> str | None:
        
        licenses = data.get("license") or []
        license_url = first_license_url(licenses)
        primary_url = deep_get(data, "resource", "primary", "URL")
        landing_url = data.get("URL")
        full_text_links = data.get("link") or []
        assertions = data.get("assertion") or []
        parts = []
        if is_open_license(license_url):
                parts.append("Acesso aberto sob licença identificada")
        elif is_tdm_license(license_url):
                parts.append("Acesso ao conteúdo sujeito à licença de mineração/texto e dados do editor")
        elif license_url:
                parts.append("Acesso condicionado à licença informada pelo editor")
        else:
                parts.append("Condições de acesso não explicitadas no registro")
        
        # 2. Registrar URL de licença, se existir
        if license_url:
                parts.append(f"Licença: {license_url}")
        
        # 3. Data de início da licença, se existir
        license_start = extract_license_start_date(licenses)
        if license_start:
                parts.append(f"Vigência da licença a partir de {license_start}")
                
        # 4. Links de texto completo
        if isinstance(full_text_links, list) and full_text_links:
                content_types = []
                for item in full_text_links:
                        if isinstance(item, dict):
                                ct = item.get("content-type")
                                if ct:
                                        content_types.append(ct)
                if content_types:
                        uniq = ", ".join(sorted(set(content_types)))
                        parts.append(f"Links de conteúdo identificados: {uniq}")
                else:
                        parts.append("Links de conteúdo identificados, mas sem tipo definido")
        
        # 5. URLs principais
        preferred_url = primary_url or landing_url
        if preferred_url:
                host = urlparse(preferred_url).netloc or preferred_url
                parts.append(f"URL principal no domínio {host}")
        
        # 6. Assertions eventualmente úteis
        access_assertions = []
        for item in assertions:
                if not isinstance(item, dict):
                        continue
                label = (item.get("label") or "").strip().lower()
                name = (item.get("name") or "").strip()
                value = (item.get("value") or "").strip()
                text = " ".join(x for x in [label, name, value] if x).lower()
                if any(term in text for term in ["open access", "access", "license", "copyright"]):
                        access_assertions.append(" ".join(x for x in [name, value] if x).strip())
        if access_assertions:
                parts.append("Informações adicionais: " + "; ".join(a for a in access_assertions if a))
                
        return " | ".join(parts) if parts else None

def infer_free_access(data: dict) -> bool | None:
    """
    Infere se a publicação é acessível gratuitamente a partir do payload Crossref.

    Retorno:
      True  -> forte evidência de acesso livre
      False -> forte evidência de acesso restrito
      None  -> não foi possível inferir com segurança
    """
    if not isinstance(data, dict):
        return None

    # 1. Licença é o melhor sinal disponível
    license_url = first_license_url(data.get("license"))

    if is_open_license(license_url):
        return True

    # if is_tdm_license(license_url):
    #     return False

    # 2. Links associados ao conteúdo
    links = data.get("link")
    if isinstance(links, list) and links:
        results = []
        for item in links:
            # print("Analisando link:", item)
            result = _link_says_free(item)
            # print("Resultado da análise do link:", result)
            if result is not None:
                results.append(result)

        if True in results:
            return True
        if results and all(r is False for r in results):
            return False

    # 3. Assertions
            assertion_result = _assertions_say_open_access(data.get("assertion"))
            if assertion_result is not None:
                return assertion_result

    # 4. URL sozinha não é prova suficiente
    return None