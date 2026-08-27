import os
import subprocess

html_content = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Guía de Estudio: Lenguajes, Compiladores, Autómatas y ANTLR 4</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@300;400;500;600;700;800&display=swap');

    @page {
        size: A4;
        margin: 1.6cm 1.4cm 1.8cm 1.4cm;
        @bottom-right {
            content: "Página " counter(page);
            font-family: 'Inter', sans-serif;
            font-size: 8.5pt;
            color: #64748b;
        }
        @bottom-left {
            content: "Guía de Estudio: Lenguajes y Compiladores · Parcial";
            font-family: 'Inter', sans-serif;
            font-size: 8.5pt;
            color: #94a3b8;
        }
    }

    * {
        box-sizing: border-box;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }

    body {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: #1e293b;
        background-color: #ffffff;
        line-height: 1.55;
        font-size: 10pt;
        margin: 0;
        padding: 0;
    }

    h1, h2, h3, h4 {
        color: #0f172a;
        font-weight: 700;
        line-height: 1.25;
        margin-top: 1.2em;
        margin-bottom: 0.4em;
        page-break-after: avoid;
    }

    h1 {
        font-size: 19pt;
        border-bottom: 3px solid #2563eb;
        padding-bottom: 6px;
        margin-top: 0;
    }

    h2 {
        font-size: 13.5pt;
        color: #1e40af;
        border-bottom: 1.5px solid #e2e8f0;
        padding-bottom: 4px;
        margin-top: 1.4em;
        page-break-after: avoid;
    }

    h3 {
        font-size: 11pt;
        color: #0f766e;
        margin-top: 1em;
        page-break-after: avoid;
    }

    p {
        margin: 0.5em 0;
        text-align: justify;
    }

    /* Portada / Encabezado */
    .header-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 60%, #3b82f6 100%);
        color: white;
        padding: 22px 24px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .header-banner h1 {
        color: white;
        border: none;
        font-size: 20pt;
        margin: 0 0 4px 0;
        padding: 0;
    }

    .header-banner p {
        color: #dbeafe;
        font-size: 10pt;
        margin: 3px 0;
    }

    .badge-container {
        margin-top: 10px;
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
    }

    .badge {
        background: rgba(255, 255, 255, 0.22);
        border: 1px solid rgba(255, 255, 255, 0.35);
        padding: 3px 9px;
        border-radius: 16px;
        font-size: 8pt;
        font-weight: 600;
        color: #ffffff;
    }

    /* Cajas destacadas */
    .box {
        border-radius: 8px;
        padding: 10px 14px;
        margin: 12px 0;
        page-break-inside: avoid;
        font-size: 9.5pt;
    }

    .box-concept {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        color: #1e3a8a;
    }

    .box-exam {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        color: #991b1b;
    }

    .box-tip {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        color: #166534;
    }

    .box-analogia {
        background-color: #faf5ff;
        border-left: 4px solid #a855f7;
        color: #6b21a8;
    }

    .box-title {
        font-weight: 700;
        font-size: 10pt;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Tablas */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 12px 0;
        font-size: 9pt;
        page-break-inside: avoid;
    }

    th, td {
        border: 1px solid #cbd5e1;
        padding: 6px 8px;
        text-align: left;
    }

    th {
        background-color: #f1f5f9;
        color: #0f172a;
        font-weight: 700;
    }

    tr:nth-child(even) {
        background-color: #f8fafc;
    }

    /* Código */
    pre, code {
        font-family: 'Fira Code', Consolas, monospace;
    }

    code {
        background-color: #f1f5f9;
        color: #0f172a;
        padding: 1px 4px;
        border-radius: 4px;
        font-size: 8.5pt;
        border: 1px solid #e2e8f0;
    }

    pre {
        background-color: #0f172a;
        color: #f8fafc;
        padding: 10px 12px;
        border-radius: 6px;
        font-size: 8.2pt;
        line-height: 1.4;
        overflow-x: auto;
        margin: 10px 0;
        page-break-inside: avoid;
    }

    pre code {
        background: transparent;
        color: inherit;
        padding: 0;
        border: none;
        font-size: inherit;
    }

    .kw { color: #f472b6; font-weight: bold; }
    .fn { color: #38bdf8; }
    .str { color: #a3e635; }
    .cm { color: #94a3b8; font-style: italic; }
    .tp { color: #fbbf24; }

    .page-break {
        page-break-before: always;
    }

    .two-cols {
        display: flex;
        gap: 12px;
        margin: 8px 0;
        page-break-inside: avoid;
    }

    .col {
        flex: 1;
    }

    ul, ol {
        margin: 0.4em 0;
        padding-left: 1.3em;
    }

    li {
        margin-bottom: 0.25em;
    }

    .q-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 10px 12px;
        margin-bottom: 10px;
        page-break-inside: avoid;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }

    .q-num {
        font-weight: 700;
        color: #2563eb;
    }

    .q-ans {
        margin-top: 5px;
        padding: 6px 8px;
        background: #f8fafc;
        border-left: 3px solid #10b981;
        border-radius: 4px;
        font-size: 9pt;
    }

    .diagram-container {
        text-align: center;
        margin: 10px 0;
        page-break-inside: avoid;
    }
    
    svg {
        max-width: 100%;
        height: auto;
    }
</style>
</head>
<body>

<!-- ENCABEZADO PRINCIPAL -->
<div class="header-banner">
    <h1>GUÍA MAESTRA DE ESTUDIO PARA EL PARCIAL</h1>
    <p><strong>Materia:</strong> Lenguajes de Programación y Transducción / Compiladores</p>
    <p><strong>Equipo:</strong> Dylan Torres · Juan Gomez · Javier Rosero</p>
    <div class="badge-container">
        <span class="badge">1. Teoría de Lenguajes</span>
        <span class="badge">2. Arquitectura del Compilador</span>
        <span class="badge">3. Estructuras de Datos</span>
        <span class="badge">4. Léxico, Regex & Autómatas</span>
        <span class="badge">5. ANTLR 4 & Visitor</span>
        <span class="badge">6. Banco de Preguntas</span>
    </div>
</div>

<!-- ========================================================================= -->
<!-- MÓDULO 1: TEORÍA DE LENGUAJES -->
<!-- ========================================================================= -->
<h2>1. Teoría de Lenguajes y Gramáticas Formales</h2>

<p>Un lenguaje en ciencias de la computación es un conjunto de cadenas formadas por símbolos tomados de un alfabeto específico bajo reglas sintácticas precisas.</p>

<div class="two-cols">
    <div class="col">
        <div class="box box-concept">
            <div class="box-title">📌 Elementos Matemáticos Básicos</div>
            <ul>
                <li><strong>Alfabeto (&Sigma;):</strong> Conjunto finito no vacío de símbolos.<br><em>Ej:</em> &Sigma; = {0, 1} (binario), &Sigma; = {a, b, c}.</li>
                <li><strong>Símbolo:</strong> Elemento atómico indivisible de &Sigma;.</li>
                <li><strong>Cadena / Palabra (w):</strong> Secuencia finita de símbolos de &Sigma;.<br><em>Longitud |w|:</em> Cantidad de símbolos (|101| = 3).</li>
                <li><strong>Cadena Vacía (&epsilon; o &lambda;):</strong> Cadena de longitud cero (|&epsilon;| = 0).</li>
                <li><strong>Lenguaje (L):</strong> Cualquier subconjunto de &Sigma;* (L &subseteq; &Sigma;*).</li>
            </ul>
        </div>
    </div>
    <div class="col">
        <div class="box box-concept">
            <div class="box-title">⚙️ Operaciones Fundamentales</div>
            <ul>
                <li><strong>Concatenación (uv):</strong> Si u = ab y v = cd &rArr; uv = abcd.</li>
                <li><strong>Potencia (w<sup>n</sup>):</strong> Repetición n veces (a<sup>3</sup> = aaa, w<sup>0</sup> = &epsilon;).</li>
                <li><strong>Unión (L<sub>1</sub> &cup; L<sub>2</sub>):</strong> Cadenas en L<sub>1</sub> o en L<sub>2</sub>.</li>
                <li><strong>Cerradura de Kleene (L*):</strong> 0 o más repeticiones de L. <em>¡Siempre contiene a &epsilon;!</em></li>
                <li><strong>Cerradura Positiva (L<sup>+</sup>):</strong> 1 o más repeticiones (L<sup>+</sup> = L L*).</li>
            </ul>
        </div>
    </div>
</div>

<h3>Jerarquía de Chomsky (Clasificación de Gramáticas y Autómatas)</h3>
<p>Noam Chomsky clasificó todas las gramáticas y lenguajes formales en 4 niveles concéntricos según el poder de sus reglas de producción:</p>

<table>
    <thead>
        <tr>
            <th>Tipo</th>
            <th>Nombre del Lenguaje</th>
            <th>Forma de las Producciones</th>
            <th>Autómata que lo Reconoce</th>
            <th>Aplicación en Compiladores</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Tipo 3</strong></td>
            <td><strong>Lenguajes Regulares</strong></td>
            <td>A &rarr; aB o A &rarr; a</td>
            <td><strong>Autómata Finito (AFD / AFND)</strong></td>
            <td><strong>Análisis Léxico</strong> (Tokens, Identificadores, Regex).</td>
        </tr>
        <tr>
            <td><strong>Tipo 2</strong></td>
            <td><strong>Libres de Contexto (GLC)</strong></td>
            <td>A &rarr; &alpha; (A es 1 no terminal)</td>
            <td><strong>Autómata de Pila (Pushdown)</strong></td>
            <td><strong>Análisis Sintáctico</strong> (Gramáticas, Parsers, ANTLR).</td>
        </tr>
        <tr>
            <td><strong>Tipo 1</strong></td>
            <td>Sensibles al Contexto</td>
            <td>&alpha;A&beta; &rarr; &alpha;&gamma;&beta; (|&gamma;| &ge; |A|)</td>
            <td>Autómata Linealmente Acotado</td>
            <td><strong>Análisis Semántico</strong> (Chequeo de tipos).</td>
        </tr>
        <tr>
            <td><strong>Tipo 0</strong></td>
            <td>Recursivamente Enumerables</td>
            <td>&alpha; &rarr; &beta; (Sin restricciones)</td>
            <td>Máquina de Turing</td>
            <td>Computabilidad Universal general.</td>
        </tr>
    </tbody>
</table>

<div class="box box-exam">
    <div class="box-title">🚨 Pregunta Fija de Parcial: ¿Por qué un Lexer (Regex) no puede contar paréntesis balanceados?</div>
    <p>Un autómata finito (Tipo 3 / Regex) solo tiene <strong>memoria finita (sus estados)</strong>. Para verificar estructuras anidadas arbitrariamente como <code>((((...))))</code> o <code>a<sup>n</sup>b<sup>n</sup></code> se requiere <strong>memoria estructurada infinita (una Pila)</strong>, lo cual pertenece a las Gramáticas Libres de Contexto (Tipo 2). Por eso el Lexer solo produce tokens y el <strong>Parser</strong> analiza la estructura jerárquica.</p>
</div>

<!-- ========================================================================= -->
<!-- MÓDULO 2: COMPILADORES Y PIPELINE -->
<!-- ========================================================================= -->
<div class="page-break"></div>
<h2>2. Arquitectura de Compiladores: Fases y Pipeline</h2>

<div class="box box-analogia">
    <div class="box-title">💡 Analogía Intuitiva del Compilador</div>
    <p>Un compilador es como un traductor profesional de libros: primero verifica que las letras formen palabras válidas en el diccionario (Léxico), luego revisa que las oraciones tengan sujeto y predicado correctos (Sintáctico), después comprueba que la historia tenga sentido lógico y coherencia de personajes (Semántico), traduce a un borrador universal (Código Intermedio), optimiza frases redundantes (Optimización) y finalmente imprime el libro en el formato final de la imprenta (Código Máquina).</p>
</div>

<h3>El Pipeline Completo del Compilador</h3>

<div class="diagram-container">
<svg width="680" height="230" viewBox="0 0 680 230" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="#000" flood-opacity="0.1"/>
    </filter>
  </defs>
  
  <!-- Frontend Box -->
  <rect x="10" y="10" width="315" height="150" rx="8" fill="#eff6ff" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="4"/>
  <text x="25" y="30" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1e40af">FRONTEND (Independiente de la máquina)</text>
  
  <!-- Backend Box -->
  <rect x="345" y="10" width="325" height="150" rx="8" fill="#f0fdf4" stroke="#22c55e" stroke-width="1.5" stroke-dasharray="4"/>
  <text x="360" y="30" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#166534">BACKEND (Dependiente de la arquitectura)</text>

  <!-- Step 1: Lexer -->
  <rect x="25" y="45" width="85" height="50" rx="5" fill="#2563eb" filter="url(#shadow)"/>
  <text x="67" y="66" font-family="Inter, sans-serif" font-size="9.5" font-weight="bold" fill="#fff" text-anchor="middle">1. Léxico</text>
  <text x="67" y="82" font-family="Inter, sans-serif" font-size="7.5" fill="#dbeafe" text-anchor="middle">Scanner / Tokens</text>
  
  <!-- Arrow 1->2 -->
  <line x1="110" y1="70" x2="128" y2="70" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
  <polygon points="128,66 136,70 128,74" fill="#64748b"/>

  <!-- Step 2: Parser -->
  <rect x="136" y="45" width="85" height="50" rx="5" fill="#2563eb" filter="url(#shadow)"/>
  <text x="178" y="66" font-family="Inter, sans-serif" font-size="9.5" font-weight="bold" fill="#fff" text-anchor="middle">2. Sintáctico</text>
  <text x="178" y="82" font-family="Inter, sans-serif" font-size="7.5" fill="#dbeafe" text-anchor="middle">Parser / AST</text>

  <!-- Arrow 2->3 -->
  <polygon points="230,66 238,70 230,74" fill="#64748b"/>
  <line x1="221" y1="70" x2="230" y2="70" stroke="#64748b" stroke-width="2"/>

  <!-- Step 3: Semantic -->
  <rect x="238" y="45" width="75" height="50" rx="5" fill="#2563eb" filter="url(#shadow)"/>
  <text x="275" y="66" font-family="Inter, sans-serif" font-size="9.5" font-weight="bold" fill="#fff" text-anchor="middle">3. Semántico</text>
  <text x="275" y="82" font-family="Inter, sans-serif" font-size="7.5" fill="#dbeafe" text-anchor="middle">Tipos / Scopes</text>

  <!-- Arrow Frontend -> Backend -->
  <polygon points="338,66 348,70 338,74" fill="#0f172a"/>
  <line x1="313" y1="70" x2="340" y2="70" stroke="#0f172a" stroke-width="2.5"/>

  <!-- Step 4: IR Code -->
  <rect x="355" y="45" width="90" height="50" rx="5" fill="#16a34a" filter="url(#shadow)"/>
  <text x="400" y="66" font-family="Inter, sans-serif" font-size="9.5" font-weight="bold" fill="#fff" text-anchor="middle">4. Código IR</text>
  <text x="400" y="82" font-family="Inter, sans-serif" font-size="7.5" fill="#dcfce7" text-anchor="middle">3 Direcciones / TAC</text>

  <!-- Arrow 4->5 -->
  <polygon points="453,66 461,70 453,74" fill="#64748b"/>
  <line x1="445" y1="70" x2="455" y2="70" stroke="#64748b" stroke-width="2"/>

  <!-- Step 5: Optimizer -->
  <rect x="461" y="45" width="90" height="50" rx="5" fill="#16a34a" filter="url(#shadow)"/>
  <text x="506" y="66" font-family="Inter, sans-serif" font-size="9.5" font-weight="bold" fill="#fff" text-anchor="middle">5. Optimización</text>
  <text x="506" y="82" font-family="Inter, sans-serif" font-size="7.5" fill="#dcfce7" text-anchor="middle">Velocidad / Espacio</text>

  <!-- Arrow 5->6 -->
  <polygon points="559,66 567,70 559,74" fill="#64748b"/>
  <line x1="551" y1="70" x2="561" y2="70" stroke="#64748b" stroke-width="2"/>

  <!-- Step 6: Code Gen -->
  <rect x="567" y="45" width="90" height="50" rx="5" fill="#16a34a" filter="url(#shadow)"/>
  <text x="612" y="66" font-family="Inter, sans-serif" font-size="9.5" font-weight="bold" fill="#fff" text-anchor="middle">6. Código Final</text>
  <text x="612" y="82" font-family="Inter, sans-serif" font-size="7.5" fill="#dcfce7" text-anchor="middle">Asm / Binario</text>

  <!-- Transversal: Symbol Table & Errors -->
  <rect x="10" y="175" width="660" height="42" rx="6" fill="#f8fafc" stroke="#64748b" stroke-width="1.2"/>
  <text x="340" y="193" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#0f172a" text-anchor="middle">COMPONENTES TRANSVERSALES (Comunicación con todas las fases)</text>
  <text x="340" y="208" font-family="Inter, sans-serif" font-size="8.5" fill="#475569" text-anchor="middle">Tabla de Símbolos (Gestión de Identificadores) &nbsp;&bull;&nbsp; Manejador y Recuperador de Errores</text>
</svg>
</div>

<h3>Descripción Detallada de cada Fase</h3>
<ol>
    <li><strong>Análisis Léxico (Lexer):</strong> Lee los caracteres del archivo de entrada y los agrupa en <strong>Tokens</strong> (tuplas como <code>&lt;ID, "resultado"&gt;</code>, <code>&lt;NUMBER, 42.5&gt;</code>). Descarta comentarios y espacios en blanco.</li>
    <li><strong>Análisis Sintáctico (Parser):</strong> Comprueba que la secuencia de tokens cumpla la estructura jerárquica de la gramática. Construye el <strong>Árbol de Sintaxis Abstracta (AST)</strong>.</li>
    <li><strong>Análisis Semántico:</strong> Valida el significado: comprobación de tipos (no sumar cadenas con booleanos), detección de variables no declaradas o duplicadas, y verificación de parámetros de funciones.</li>
    <li><strong>Generación de Código Intermedio (IR):</strong> Produce una representación intermedia independiente del hardware, típicamente en <strong>Código de Tres Direcciones (TAC)</strong> como <code>t1 = a + b</code>, <code>t2 = t1 * c</code>.</li>
    <li><strong>Optimización de Código:</strong> Aplica técnicas como: <em>Propagación de Constantes</em> (calcular <code>3 * 5</code> en compilación como <code>15</code>), <em>Eliminación de Código Muerto</em> (código inalcanzable), y <em>Reducción de Fuerza</em> (cambiar <code>x * 2</code> por <code>x + x</code> o desplazamiento de bits).</li>
    <li><strong>Generación de Código Final:</strong> Emite código ensamblador o binario para la arquitectura del procesador (x86_64, ARM) asignando registros de CPU de forma eficiente.</li>
</ol>

<!-- ========================================================================= -->
<!-- MÓDULO 3: ESTRUCTURAS DE DATOS EN COMPILADORES -->
<!-- ========================================================================= -->
<div class="page-break"></div>
<h2>3. Estructuras de Datos en Compiladores</h2>

<p>El rendimiento y la modularidad de un compilador dependen de 4 estructuras de datos fundamentales:</p>

<table>
    <thead>
        <tr>
            <th>Estructura</th>
            <th>Fase Principal</th>
            <th>Propósito y Funcionamiento</th>
            <th>Implementación en Memoria</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Tabla de Símbolos</strong></td>
            <td>Todas las fases</td>
            <td>Guarda los identificadores (variables, funciones, clases) junto con sus atributos: nombre, tipo, ámbito (scope), dirección de memoria y valor.</td>
            <td><code>Map&lt;String, Symbol&gt;</code> o tablas hash encadenadas para soporte de ámbitos anidados.</td>
        </tr>
        <tr>
            <td><strong>Parse Tree (CST)</strong></td>
            <td>Sintáctico</td>
            <td>Árbol sintáctico concreto que contiene absolutamente <em>todos</em> los elementos del texto fuente (incluyendo paréntesis y comas).</td>
            <td>Estructura de árbol n-ario generada automáticamente por ANTLR.</td>
        </tr>
        <tr>
            <td><strong>AST (Abstract Syntax Tree)</strong></td>
            <td>Semántico e IR</td>
            <td>Árbol sintáctico abstracto simplificado. Elimina la puntuación superflua y conserva solo operadores y operandos esenciales.</td>
            <td>Nodos de clases polimórficas (<code>BinaryExpr</code>, <code>NumberLiteral</code>).</td>
        </tr>
        <tr>
            <td><strong>Pila de Parsing (Stack)</strong></td>
            <td>Parsers LL / LR</td>
            <td>Gestiona el seguimiento del estado de la gramática, llamadas a funciones y evaluación de expresiones en notación postfija.</td>
            <td>Estructura LIFO (<code>Stack&lt;T&gt;</code> / <code>Deque&lt;T&gt;</code>).</td>
        </tr>
    </tbody>
</table>

<h3>Comparación Visual: Parse Tree (CST) vs AST para <code>(3 + 5) * 2</code></h3>

<div class="diagram-container">
<svg width="600" height="150" viewBox="0 0 600 150" xmlns="http://www.w3.org/2000/svg">
  <!-- CST Left -->
  <text x="140" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#1e40af" text-anchor="middle">Parse Tree (CST - Concreto)</text>
  <circle cx="140" cy="40" r="14" fill="#dbeafe" stroke="#2563eb" stroke-width="1.5"/>
  <text x="140" y="44" font-family="Inter, sans-serif" font-size="10" font-weight="bold" fill="#1e40af" text-anchor="middle">expr</text>
  
  <line x1="130" y1="52" x2="80" y2="85" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="140" y1="54" x2="140" y2="85" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="150" y1="52" x2="200" y2="85" stroke="#94a3b8" stroke-width="1.5"/>
  
  <circle cx="80" cy="95" r="12" fill="#eff6ff" stroke="#3b82f6"/>
  <text x="80" y="99" font-family="Inter, sans-serif" font-size="9" fill="#1e3a8a" text-anchor="middle">(</text>
  
  <circle cx="140" cy="95" r="14" fill="#dbeafe" stroke="#2563eb"/>
  <text x="140" y="99" font-family="Inter, sans-serif" font-size="9" font-weight="bold" fill="#1e40af" text-anchor="middle">expr (+)</text>

  <circle cx="200" cy="95" r="12" fill="#eff6ff" stroke="#3b82f6"/>
  <text x="200" y="99" font-family="Inter, sans-serif" font-size="9" fill="#1e3a8a" text-anchor="middle">* 2 )</text>

  <!-- AST Right -->
  <text x="440" y="18" font-family="Inter, sans-serif" font-size="11" font-weight="bold" fill="#166534" text-anchor="middle">AST (Abstract Syntax Tree - Abstracto)</text>
  <circle cx="440" cy="45" r="16" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>
  <text x="440" y="50" font-family="Fira Code, monospace" font-size="13" font-weight="bold" fill="#166534" text-anchor="middle">*</text>

  <line x1="428" y1="58" x2="390" y2="95" stroke="#64748b" stroke-width="1.8"/>
  <line x1="452" y1="58" x2="490" y2="95" stroke="#64748b" stroke-width="1.8"/>

  <circle cx="390" cy="105" r="14" fill="#dcfce7" stroke="#16a34a" stroke-width="1.5"/>
  <text x="390" y="110" font-family="Fira Code, monospace" font-size="12" font-weight="bold" fill="#166534" text-anchor="middle">+</text>

  <circle cx="490" cy="105" r="14" fill="#f1f5f9" stroke="#64748b" stroke-width="1.5"/>
  <text x="490" y="109" font-family="Fira Code, monospace" font-size="11" fill="#0f172a" text-anchor="middle">2</text>

  <line x1="380" y1="116" x2="360" y2="135" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="400" y1="116" x2="420" y2="135" stroke="#94a3b8" stroke-width="1.5"/>

  <circle cx="360" cy="140" r="10" fill="#f1f5f9" stroke="#64748b"/>
  <text x="360" y="144" font-family="Fira Code, monospace" font-size="9" fill="#0f172a" text-anchor="middle">3</text>

  <circle cx="420" cy="140" r="10" fill="#f1f5f9" stroke="#64748b"/>
  <text x="420" y="144" font-family="Fira Code, monospace" font-size="9" fill="#0f172a" text-anchor="middle">5</text>
</svg>
</div>

<!-- ========================================================================= -->
<!-- MÓDULO 4: ANÁLISIS LÉXICO, REGEX Y AUTÓMATAS -->
<!-- ========================================================================= -->
<div class="page-break"></div>
<h2>4. Análisis Léxico, Expresiones Regulares y Autómatas (AFD / AFND)</h2>

<p>La base teórica del análisis léxico se fundamenta en la equivalencia matemática entre las <strong>Expresiones Regulares (ER)</strong>, los <strong>Autómatas Finitos No Deterministas (AFND)</strong> y los <strong>Autómatas Finitos Deterministas (AFD)</strong>.</p>

<h3>1. Definición Formal de un Autómata Finito Determinista (AFD)</h3>
<p>Un AFD es una 5-tupla: <strong>M = (Q, &Sigma;, &delta;, q<sub>0</sub>, F)</strong> donde:</p>
<ul>
    <li><strong>Q:</strong> Conjunto finito y no vacío de estados.</li>
    <li><strong>&Sigma;:</strong> Alfabeto de entrada.</li>
    <li><strong>&delta;:</strong> Función de transición total <code>&delta;: Q &times; &Sigma; &rarr; Q</code> (para cada estado y cada símbolo existe exactamente un estado destino).</li>
    <li><strong>q<sub>0</sub> &isin; Q:</strong> Estado inicial único.</li>
    <li><strong>F &subseteq; Q:</strong> Conjunto de estados de aceptación o finales (representados con doble círculo).</li>
</ul>

<h3>2. Algoritmo de Thompson: De Expresión Regular a AFND</h3>
<p>Permite construir sistemáticamente un AFND con transiciones &epsilon; para cualquier operador de una expresión regular:</p>

<table>
    <thead>
        <tr>
            <th>Operación</th>
            <th>Expresión Regular</th>
            <th>Construcción de Thompson (Esquema del Autómata)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Símbolo Básico</strong></td>
            <td><code>a</code></td>
            <td><code>(inicio) ─── a ───&gt; ((final))</code></td>
        </tr>
        <tr>
            <td><strong>Concatenación</strong></td>
            <td><code>ab</code></td>
            <td><code>(inicio) ──[ a ]──&gt; (medio) ──[ b ]──&gt; ((final))</code></td>
        </tr>
        <tr>
            <td><strong>Unión (Alternativa)</strong></td>
            <td><code>a | b</code></td>
            <td><code>(inicio) ┬── &epsilon; ──&gt; [ a ] ── &epsilon; ──┬──&gt; ((final))<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── &epsilon; ──&gt; [ b ] ── &epsilon; ──┘</code></td>
        </tr>
        <tr>
            <td><strong>Cerradura de Kleene</strong></td>
            <td><code>a*</code></td>
            <td><code>(inicio) ┬── &epsilon; ──&gt; [ a ] ── &epsilon; ──┬──&gt; ((final))<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;▲&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── &epsilon; ───┘&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──────────── &epsilon; ─────────────┘</code></td>
        </tr>
    </tbody>
</table>

<h3>3. Algoritmo de Construcción de Subconjuntos (De AFND a AFD)</h3>
<p>Como las computadoras no pueden procesar transiciones múltiples simultáneas (&epsilon;), se aplica la construcción de subconjuntos:</p>
<ul>
    <li><strong>&epsilon;-clausura(s):</strong> Conjunto de todos los estados alcanzables desde <em>s</em> usando únicamente transiciones &epsilon; (incluyendo al propio <em>s</em>).</li>
    <li><strong>mueve(T, a):</strong> Conjunto de estados a los que se llega desde cualquier estado del conjunto <em>T</em> consumiendo el símbolo <em>a</em>.</li>
    <li><strong>Transición en el AFD:</strong> <code>&delta;<sub>AFD</sub>(T, a) = &epsilon;-clausura(mueve(T, a))</code>.</li>
</ul>

<div class="box box-tip">
    <div class="box-title">📝 Ejemplo Resuelto de Parcial: Regex para Identificadores y Decimales</div>
    <ul>
        <li><strong>Identificador:</strong> <code>[a-zA-Z_][a-zA-Z0-9_]*</code> (Inicia con letra o guion bajo, seguido de letras, dígitos o guiones bajos).</li>
        <li><strong>Número Decimal / Real:</strong> <code>[0-9]+ ('.' [0-9]+)?</code> (Uno o más dígitos enteros, opcionalmente seguidos de un punto y más dígitos).</li>
    </ul>
</div>

<!-- ========================================================================= -->
<!-- MÓDULO 5: ANTLR 4 Y PATRÓN VISITOR -->
<!-- ========================================================================= -->
<div class="page-break"></div>
<h2>5. ANTLR 4: Gramáticas, Precedencia, Listener y Visitor</h2>

<p><strong>ANTLR 4 (ANother Tool for Language Recognition)</strong> es el generador de analizadores sintácticos más potente de la industria. Utiliza algoritmos <strong>ALL(*)</strong>, resolviendo de forma nativa la precedencia de operadores y la recursión izquierda directa.</p>

<h3>1. Estructura de una Gramática en ANTLR 4 (<code>ScientificCalc.g4</code>)</h3>

<pre><code><span class="kw">grammar</span> ScientificCalc;

<span class="cm">// ==================== REGLAS DEL PARSER (Inician con MINÚSCULA) ====================</span>
prog: stat+ ;

stat: expr NEWLINE                 <span class="str"># printExpr</span>
    | ID <span class="str">'='</span> expr NEWLINE          <span class="str"># assign</span>
    | <span class="str">'clear'</span> NEWLINE              <span class="str"># clearMem</span>
    ;

<span class="cm">// En ANTLR 4 la precedencia se define POR EL ORDEN DE LAS REGLAS (Arriba = Mayor prioridad)</span>
expr: <span class="str">'('</span> expr <span class="str">')'</span>                 <span class="str"># parens</span>
    | <span class="str">'&lt;assoc=right&gt;'</span> expr <span class="str">'^'</span> expr <span class="str"># power</span>       <span class="cm">// Mayor precedencia: Potencia a la derecha</span>
    | (<span class="str">'+'</span>|<span class="str">'-'</span>) expr              <span class="str"># unarySign</span>   <span class="cm">// Signo unario</span>
    | expr op=(<span class="str">'*'</span>|<span class="str">'/'</span>) expr       <span class="str"># mulDiv</span>      <span class="cm">// Multiplicación y División</span>
    | expr op=(<span class="str">'+'</span>|<span class="str">'-'</span>) expr       <span class="str"># addSub</span>      <span class="cm">// Menor precedencia: Suma y Resta</span>
    | function <span class="str">'('</span> expr <span class="str">')'</span>        <span class="str"># funcCall</span>
    | ID                           <span class="str"># id</span>
    | NUMBER                       <span class="str"># num</span>
    ;

function: <span class="str">'sin'</span> | <span class="str">'cos'</span> | <span class="str">'tan'</span> | <span class="str">'sqrt'</span> | <span class="str">'log'</span> | <span class="str">'ln'</span> | <span class="str">'abs'</span> ;

<span class="cm">// ==================== REGLAS DEL LEXER (Inician con MAYÚSCULA) ====================</span>
NUMBER  : [0-9]+ (<span class="str">'.'</span> [0-9]+)? ;
ID      : [a-zA-Z_][a-zA-Z0-9_]* ;
NEWLINE : <span class="str">'\r'</span>? <span class="str">'\n'</span> ;
WS      : [ \t]+ -&gt; <span class="kw">skip</span> ;  <span class="cm">// La directiva skip descarta espacios y tabulaciones</span></code></pre>

<h3>2. Las 4 Reglas de Oro de ANTLR 4</h3>
<ol>
    <li><strong>Diferenciación Léxico / Sintáctico:</strong> Reglas con <strong>MAYÚSCULA</strong> son del Lexer (tokens); reglas con <strong>minúscula</strong> son del Parser.</li>
    <li><strong>Precedencia de Operadores:</strong> Las alternativas escritas más arriba en la regla <code>expr</code> tienen mayor prioridad matemática.</li>
    <li><strong>Asociatividad:</strong> Por defecto es a la izquierda (<code>1 - 2 - 3</code> = <code>(1 - 2) - 3</code>). Para potencias se usa explícitamente <code>&lt;assoc=right&gt;</code> (<code>2 ^ 3 ^ 2</code> = <code>2 ^ (3 ^ 2)</code> = 512).</li>
    <li><strong>Etiquetas de Alternativa (<code># etiqueta</code>):</strong> Generan métodos específicos en el Visitor (ej. <code>visitAddSub</code>, <code>visitPower</code>), permitiendo un código desacoplado y sin <code>if-else</code> gigantes.</li>
</ol>

<h3>3. Patrón Visitor vs Patrón Listener</h3>

<table>
    <thead>
        <tr>
            <th>Característica</th>
            <th>Patrón Visitor (Recomendado para Evaluadores)</th>
            <th>Patrón Listener (Recomendado para Traductores/Linters)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Control del Recorrido</strong></td>
            <td><strong>Manual / Explícito.</strong> Tú decides cuándo y cómo llamar a <code>visit(nodoHijo)</code>.</td>
            <td><strong>Automático / Pasivo.</strong> Un <code>ParseTreeWalker</code> recorre todo el árbol en profundidad.</td>
        </tr>
        <tr>
            <td><strong>Retorno de Valores</strong></td>
            <td><strong>Sí.</strong> Retorna tipos genéricos: <code>extends ScientificCalcBaseVisitor&lt;Double&gt;</code>.</td>
            <td><strong>No.</strong> Todos los métodos retornan <code>void</code> (requiere pilas o mapas externos).</td>
        </tr>
        <tr>
            <td><strong>Evaluación Condicional / Bucles</strong></td>
            <td><strong>Excelente.</strong> Puedes evaluar solo una rama de un <code>if</code> o evaluar 800 veces en <code>plot</code>.</td>
            <td><strong>Imposible.</strong> Siempre visita cada nodo del árbol exactamente una vez.</td>
        </tr>
        <tr>
            <td><strong>Firma de Métodos</strong></td>
            <td><code>Double visitAddSub(ScientificCalcParser.AddSubContext ctx)</code></td>
            <td><code>void enterAddSub(...)</code> y <code>void exitAddSub(...)</code></td>
        </tr>
    </tbody>
</table>

<!-- ========================================================================= -->
<!-- MÓDULO 6: BANCO DE PREGUNTAS DE PARCIAL -->
<!-- ========================================================================= -->
<div class="page-break"></div>
<h2>6. Banco de Preguntas Típicas de Examen Parcial</h2>

<div class="q-card">
    <div><span class="q-num">Pregunta 1:</span> ¿Cuál es la diferencia entre la fase de Análisis Sintáctico (Parser) y la de Análisis Semántico?</div>
    <div class="q-ans">
        <strong>Respuesta:</strong> El <strong>Parser</strong> valida que la estructura y el orden de los tokens cumplan la gramática (por ejemplo, que no falte un paréntesis o un operador). El <strong>Análisis Semántico</strong> valida el significado lógico y la congruencia de los datos (por ejemplo, que una variable esté declarada antes de usarse, o que no se intente sumar un texto con un número booleano).
    </div>
</div>

<div class="q-card">
    <div><span class="q-num">Pregunta 2:</span> ¿Qué es una gramática ambigua y por qué representa un grave problema en compiladores?</div>
    <div class="q-ans">
        <strong>Respuesta:</strong> Una gramática es ambigua si para una misma cadena de entrada existen <strong>dos o más árboles de análisis sintáctico válidos</strong>. Es un problema crítico porque un compilador no sabría qué significado semántico darle al código (ejemplo clásico: la expresión <code>2 + 3 * 4</code> podría evaluarse como <code>(2 + 3) * 4 = 20</code> o como <code>2 + (3 * 4) = 14</code>).
    </div>
</div>

<div class="q-card">
    <div><span class="q-num">Pregunta 3:</span> En ANTLR 4, ¿qué función cumple la directiva <code>-> skip</code> en las reglas del Lexer?</div>
    <div class="q-ans">
        <strong>Respuesta:</strong> Indica al Lexer que, tras reconocer los caracteres coincidentes (como espacios en blanco <code>[ \t]+</code> o comentarios), los <strong>descarte completamente</strong> y no genere un token para el Parser, manteniendo limpia la gramática sintáctica.
    </div>
</div>

<div class="q-card">
    <div><span class="q-num">Pregunta 4:</span> En un evaluador basado en el patrón Visitor, ¿por qué es fundamental tener un <code>Map&lt;String, Double&gt; memory</code>?</div>
    <div class="q-ans">
        <strong>Respuesta:</strong> Actúa como la <strong>Tabla de Símbolos en tiempo de ejecución</strong>. Permite persistir el valor de variables asignadas (ej. <code>a = 10</code>) y recuperarlas cuando se consultan en expresiones posteriores (ej. <code>a * 2</code>).
    </div>
</div>

<div class="q-card">
    <div><span class="q-num">Pregunta 5:</span> ¿Cómo logra el comando <code>plot(f(x), xmin, xmax)</code> graficar una función sin tener que recompilar la expresión matemática en cada punto?</div>
    <div class="q-ans">
        <strong>Respuesta:</strong> Aprovecha que el árbol sintáctico (AST) generado por ANTLR es inmutable en memoria. Divide el intervalo en muestras (ej. 800 puntos) y en un bucle actualiza <code>memory.put("x", valorActual)</code> e invoca <code>visit(tree)</code>, reutilizando el mismo árbol para calcular cada punto <em>(x, y)</em> en microsegundos.
    </div>
</div>

<div class="q-card">
    <div><span class="q-num">Pregunta 6:</span> ¿Qué diferencia existe entre un análisis sintáctico Top-Down (LL) y uno Bottom-Up (LR)?</div>
    <div class="q-ans">
        <strong>Respuesta:</strong> <strong>Top-Down (LL):</strong> Construye el árbol desde la raíz (símbolo inicial) hacia las hojas (tokens), prediciendo las producciones. <strong>Bottom-Up (LR):</strong> Comienza en las hojas (tokens de entrada) y realiza operaciones de <em>desplazamiento (shift)</em> y <em>reducción (reduce)</em> hasta alcanzar la raíz.
    </div>
</div>

<div class="box box-tip">
    <div class="box-title">🚀 Resumen de Fórmulas y Reglas Mnemotécnicas para el Parcial</div>
    <ul>
        <li><strong>Jerarquía:</strong> Regulares (AF) &sub; Libres de Contexto (Pila) &sub; Sensibles al Contexto &sub; Enumerables (Turing).</li>
        <li><strong>Thompson:</strong> Concatenación = En serie | Unión = En paralelo con &epsilon; | Cerradura = Bucle con &epsilon;.</li>
        <li><strong>Subconjuntos:</strong> <code>Nuevo Estado = &epsilon;-clausura(mueve(EstadoActual, símbolo))</code>.</li>
        <li><strong>Precedencia en ANTLR:</strong> Lo más alto en la lista de alternativas se evalúa con mayor prioridad.</li>
        <li><strong>Visitor:</strong> Control de flujo manual, tipo de retorno genérico <code>T</code>, ideal para calculadoras y lenguajes interpretados.</li>
    </ul>
</div>

<div style="text-align: center; margin-top: 25px; padding: 10px; border-top: 1px solid #cbd5e1; color: #64748b; font-size: 8.5pt;">
    Guía de Preparación de Parcial · Lenguajes de Programación y Transducción · 2026
</div>

</body>
</html>
"""

html_path = "/home/Xavi/Escritorio/Trabajos/Materias/Lenguajes de Programacion y Transduccion/Calculadora_ANTLR4/guia_estudio/Guia_Estudio_Parcial.html"
pdf_path = "/home/Xavi/Escritorio/Trabajos/Materias/Lenguajes de Programacion y Transduccion/Calculadora_ANTLR4/Guia_Estudio_Parcial.pdf"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML generado en: {html_path}")

cmd = [
    "/usr/bin/brave-browser",
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    f"--print-to-pdf={pdf_path}",
    "--no-pdf-header-footer",
    html_path
]

print("Compilando PDF con Brave Browser...")
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0 and os.path.exists(pdf_path):
    size_kb = os.path.getsize(pdf_path) / 1024
    print(f"¡PDF generado exitosamente!: {pdf_path} ({size_kb:.1f} KB)")
else:
    print("Error generando PDF:", res.stderr)
