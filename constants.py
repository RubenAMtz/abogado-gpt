import random

QUERIES = [
    'puedo manejar un carro con placas de otro pais?',
	'cuales son las obligaciones de un oficial?',
	'me cruce un semaforo y me llevaron al juzgado, tiene esa facultad un estatal?',
	'que debo hacer si me roban el carro?',
	'es normal que te esposen por una infraccion de transito?',
	"¿Puedo estacionarme en la banqueta?",
    "¿Me puedo estacionar en sentido contrario?",
    "¿Puedo conducir con comida en la mano?",
    "¿Puedo conducir con mi mascota?",
    'me puedo estacionar en doble fila?',
    'me pueden arrestar dentro de mi casa?',
    'me pueden multar por no usar el cinturon?',
    'es normal que te esposen por una infraccion de transito?',
    'me multaron por no traer el cinturon, es correcto?',
    'me multaron por manejar en sentido contrario pero el oficial se porto muy grosero',
    'puedo manejar un carro con placas americanas?',
    'puedo manejar con licencia del extranjero?',
	'me pueden quitar mi licencia como aval para pago de una multa?',
	'que debo hacer si me arrestan por intento de robo?'
]

QUERY = random.choice(QUERIES)

ARTICLE_PATTERNS = """
ARTICULO \d+.-| ARTICULO \*\d+.- | ARTICULO \d+o.- | ARTICULO \*\d+o.- |ARTICULO \d+ BIS.-|ARTICULO \d+-[A-Z].- 
ARTÍCULO \d+.- | ARTÍCULO \d+º.- | ARTÍCULO \*\d+.- | ARTÍCULO \d+ BIS.- | ARTÍCULO \d+ BIS [A-Z].- | ARTÍCULO \d+ TER.- | ARÍCULO \d+.- | 
Artículo \d+.- | Artículo \*\d+.- | Artículo \d+o.- | Artículo \*\d+o.- | Artículo \d+º.- | Artículo \d+ BIS.- | Artículo \d+ BIS [A-Z].- | Artículo \d+ TER.- | Artículo \d+. | Artículo \*\d+. | Artículo \d+o. | Artículo \*\d+o. | Artículo \d+º. | Artículo \d+ BIS. | Artículo \d+ BIS [A-Z]. | Artículo \d+ TER. 
"""

ARTICLE_PATTERN_A = "ARTICULO \d+\.-| ARTICULO \*\d+.- | ARTICULO \d+o.- | ARTICULO \*\d+o.-|ARTICULO \d+ BIS.-|ARTICULO \d+\-[A-Z].-| T R A N S I T O R I O S(?=\s+[A-Z])"
ARTICLE_PATTERN_B = "ARTÍCULO \d+.- | ARTÍCULO \d+º.- | ARTÍCULO \*\d+.- | ARTÍCULO \d+ BIS.- | ARTÍCULO \d+ BIS [A-Z].- | ARTÍCULO \d+ TER.- | ARÍCULO \d+.-| T R A N S I T O R I O S(?=\s+[A-Z])"
ARTICLE_PATTERN_C = "Artículo \d+.- | Artículo \*\d+.- | Artículo \d+o.- | Artículo \*\d+o.- | Artículo \d+º.- | Artículo \d+ BIS.- | Artículo \d+ BIS [A-Z].- | Artículo \d+ TER.-"
ARTICLE_PATTERN_D = "Artículo \d+\. | Artículo \*\d+\. | Artículo \d+o\. | Artículo \*\d+o\. | Artículo \d+º\. | Artículo \d+ BIS\. | Artículo \d+ BIS [A-Z]\. | Artículo \d+ TER\. |\.\s+TRANSITORIOS"
ARTICLE_PATTERN_E = "ARTICULO \d+\.-| ARTICULO \*\d+.- | ARTICULO \d+o.- | ARTICULO \*\d+o.-|ARTICULO \d+ BIS.-|ARTICULO \d+\-[A-Z].-|ARTÍCULO \d+.- | ARTÍCULO \d+º.- | ARTÍCULO \*\d+.- | ARTÍCULO \d+ BIS.- | ARTÍCULO \d+ BIS [A-Z].- | ARTÍCULO \d+ TER.- | ARÍCULO \d+.-|ARTICULO \d+\.| ARTICULO \*\d+.| ARTICULO \d+o.| ARTICULO \*\d+o.|ARTICULO \d+ BIS.|ARTICULO \d+\-[A-Z].|ARTÍCULO \d+.| ARTÍCULO \d+º.| ARTÍCULO \*\d+.| ARTÍCULO \d+ BIS.| ARTÍCULO \d+ BIS [A-Z].| ARTÍCULO \d+ TER.| ARÍCULO \d+.| T R A N S I T O R I O S(?=\s+[A-Z])"
INFORME_OFICIAL_HOMOLOGADO = "PRIMERO. |SEGUNDO. |TERCERO. |CUARTO. |QUINTO. |SEXTO. |SÉPTIMO. |OCTAVO. |NOVENO. |DÉCIMO. |DÉCIMO PRIMERO. |DÉCIMO SEGUNDO. |DÉCIMO TERCERO. |DÉCIMO CUARTO. |DÉCIMO QUINTO. |DÉCIMO SEXTO. |DÉCIMO SÉPTIMO. |DÉCIMO OCTAVO. |DÉCIMO NOVENO. |VIGÉSIMO. |VIGÉSIMO PRIMERO. |VIGÉSIMO SEGUNDO. |VIGÉSIMO TERCERO. |VIGÉSIMO CUARTO. |VIGÉSIMO QUINTO. |VIGÉSIMO SEXTO. |VIGÉSIMO SÉPTIMO. |VIGÉSIMO OCTAVO. |VIGÉSIMO NOVENO. |TRIGÉSIMO. |TRIGÉSIMO PRIMERO. |TRIGÉSIMO SEGUNDO. |TRIGÉSIMO TERCERO. |TRIGÉSIMO CUARTO. |TRIGÉSIMO QUINTO. |TRIGÉSIMO SEXTO. |TRIGÉSIMO SÉPTIMO. |TRIGÉSIMO OCTAVO. |TRIGÉSIMO NOVENO. |CUADRAGÉSIMO. |CUADRAGÉSIMO PRIMERO. |CUADRAGÉSIMO SEGUNDO. |CUADRAGÉSIMO TERCERO. |CUADRAGÉSIMO CUARTO. |CUADRAGÉSIMO QUINTO. |CUADRAGÉSIMO SEXTO. |CUADRAGÉSIMO SÉPTIMO. |CUADRAGÉSIMO OCTAVO. |CUADRAGÉSIMO NOVENO. |QUINCUAGÉSIMO. |QUINCUAGÉSIMO PRIMERO. |QUINCUAGÉSIMO SEGUNDO. |QUINCUAGÉSIMO TERCERO. |QUINCUAGÉSIMO CUARTO. |QUINCUAGÉSIMO QUINTO. |QUINCUAGÉSIMO SEXTO. |QUINCUAGÉSIMO SÉPTIMO. |QUINCUAGÉSIMO OCTAVO. |QUINCUAG"

