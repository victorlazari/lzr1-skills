# Specialist: 35-spanish-teacher

## === FILE: 35-spanish-teacher-advanced.md ===
# 35 - Spanish Teacher Supreme (Advanced Pedagogical Strategies)

## 1. The Comprehensible Input Hypothesis
Stephen Krashen's hypothesis states that learners acquire language best when they receive input that is slightly above their current level of competence (i+1).
- **Application:** Use graded readers, podcasts, and simplified news for A2-B1 learners. Transition to native media (Netflix, YouTube, literature) at B2.

## 2. Spaced Repetition Systems (SRS)
To build a massive vocabulary (10,000+ words), rote memorization is inefficient. SRS algorithms (like Anki or SuperMemo) calculate the optimal time to review a word before it is forgotten.
- **Deck Strategy:** Create custom decks with full sentences rather than isolated words to provide context and grammatical structure.

## 3. The Shadowing Technique
Shadowing involves listening to native audio and repeating it aloud almost simultaneously.
- **Benefits:** Improves pronunciation, intonation, rhythm, and helps overcome the "foreign accent."
- **Execution:** Start with slow audio (e.g., News in Slow Spanish), listen once, then listen and read the transcript, then shadow without the transcript.

## 4. Language Transfer and Interference
English speakers learning Spanish often face specific challenges due to language transfer.
- **False Friends (Falsos Amigos):** "Embarazada" means pregnant, not embarrassed. "Éxito" means success, not exit. "Recordar" means to remember, not to record.
- **Prepositional Mismatches:** English "to depend on" becomes Spanish "depender de". English "to dream about" becomes Spanish "soñar con".

## 5. Advanced Subjunctive Triggers
Beyond basic emotions and desires, the subjunctive is triggered by specific conjunctions.
- **Always Subjunctive:** A menos que (unless), antes de que (before), con tal de que (provided that), en caso de que (in case), para que (so that), sin que (without).
- **Subjunctive or Indicative (Depending on context):** Cuando (when), después de que (after), en cuanto (as soon as), hasta que (until), mientras (while). Use subjunctive if the action is in the future; use indicative if it is a habitual or past action.

## 6. The Passive Voice and "Se" Impersonal
In advanced Spanish, the true passive voice (Ser + past participle) is less common than the "se" impersonal or "se" passive.
- **True Passive:** El libro fue escrito por Cervantes. (The book was written by Cervantes.)
- **Se Passive:** Se venden libros aquí. (Books are sold here.)
- **Se Impersonal:** Se dice que va a llover. (It is said that it's going to rain.)

## 7. Dialectal Mastery: Rioplatense vs. Caribbean vs. Castilian
To reach C2, a learner must understand regional variations.
- **Voseo (Argentina/Uruguay):** Use of "vos" instead of "tú". Conjugation: vos cantás, vos tenés, vos sos.
- **Aspiration of 's' (Caribbean/Andalusia):** "Los niños" becomes "Loh niño".
- **Yeísmo vs. Lleísmo:** Most regions pronounce 'll' and 'y' identically (yeísmo), but some Andean regions distinguish them, and Rioplatense pronounces them as 'sh' or 'zh' (zheísmo/sheísmo).

## === FILE: 35-spanish-teacher-cli-reference.md ===
# 35 - Spanish Teacher (CLI & Tools Reference)

While language learning doesn't have a traditional CLI, this reference covers the essential digital tools, syntax for flashcards, and prompt engineering for AI language tutors.

## 1. Anki SRS Syntax
Creating effective flashcards using Anki's bulk import formats.

### Basic CSV Import Format
```csv
Front,Back,Tags
"El perro","The dog","vocab animals"
"Yo ___ (hablar) español.","hablo","grammar present-tense"
```

### Cloze Deletion Format (Fill-in-the-blank)
```text
Text,Tags
"Ayer yo {{c1::fui}} al mercado.","grammar preterite"
"Si yo {{c1::tuviera}} dinero, {{c2::viajaría}} por el mundo.","grammar subjunctive conditional"
```

## 2. AI Tutor Prompts (ChatGPT/Claude)

### Conversation Practice
`Act as a native Spanish speaker from [Country]. Have a conversation with me at a [CEFR Level] level about [Topic]. Correct my mistakes gently after each turn and explain the grammar rule I violated.`

### Conjugation Drilling
`Generate a markdown table of the verb [Verb] in the [Tense] tense. Then, provide 5 fill-in-the-blank sentences using this verb in this tense.`

### Reading Comprehension
`Write a short story (300 words) in Spanish at a B1 level about a trip to Madrid. Include 5 comprehension questions at the end.`

## 3. Recommended Digital Tools
- **DeepL:** Superior to Google Translate for Spanish idioms and nuanced phrasing.
- **WordReference:** Excellent for seeing words in context across different regional dialects.
- **SpanishDict:** The definitive online dictionary with full conjugation tables and regional tags (e.g., [ES], [MX], [AR]).
- **Language Reactor:** Browser extension for Netflix/YouTube that provides dual subtitles and hover-translations.

## === FILE: 35-spanish-teacher-config-schemas.md ===
# 35 - Spanish Teacher (Curriculum Configuration Schemas)

This document outlines the standard curriculum progression (the "schema") for each CEFR level.

## A1 (Beginner) Schema
- **Vocabulary Target:** 500 words
- **Grammar Nodes:**
  - Present indicative (regular -ar, -er, -ir)
  - Ser vs. Estar
  - Gender and number of nouns/adjectives
  - Definite and indefinite articles
  - Numbers 0-100, days, months, seasons
  - Basic question words (qué, quién, dónde, cuándo, por qué, cómo)
  - Ir a + infinitive (informal future)
  - Tener expressions (tener hambre, tener sed, tener años)

## A2 (Elementary) Schema
- **Vocabulary Target:** 1,500 words
- **Grammar Nodes:**
  - Present indicative (irregular verbs, stem-changing verbs)
  - Reflexive verbs and daily routines
  - Preterite tense (regular and highly irregular verbs like ir, ser, hacer, tener)
  - Imperfect tense (regular and the 3 irregulars: ir, ser, ver)
  - Direct and indirect object pronouns
  - Gustar and similar verbs (encantar, importar, doler)
  - Comparatives and superlatives (más que, menos que, tan como)
  - Affirmative informal commands (tú commands)

## B1 (Intermediate) Schema
- **Vocabulary Target:** 3,000 words
- **Grammar Nodes:**
  - Preterite vs. Imperfect mastery
  - Future simple tense
  - Conditional tense
  - Present perfect (haber + past participle)
  - Introduction to the Present Subjunctive (WEIRDO verbs: Wishes, Emotions, Impersonal expressions, Recommendations, Doubt, Ojalá)
  - Por vs. Para mastery
  - Formal commands (usted/ustedes) and negative commands
  - Relative pronouns (que, quien, lo que)

## B2 (Upper Intermediate) Schema
- **Vocabulary Target:** 5,000+ words
- **Grammar Nodes:**
  - Past perfect (Pluperfect)
  - Imperfect Subjunctive (formation and usage)
  - Si clauses (If clauses) - Type 1 and Type 2
  - Subjunctive with conjunctions of time and contingency
  - The passive voice and "se" passive/impersonal
  - Future perfect and conditional perfect
  - Reported speech (El estilo indirecto)

## C1/C2 (Advanced/Mastery) Schema
- **Vocabulary Target:** 10,000+ words
- **Grammar Nodes:**
  - Pluperfect Subjunctive
  - Si clauses - Type 3 (Si hubiera sabido, habría ido)
  - Nuances of ser/estar with adjectives (ser listo = clever, estar listo = ready)
  - Regional slang, idioms, and colloquialisms
  - Complex prepositional phrases
  - Literary tenses (Pretérito anterior - rarely used but recognized)

## === FILE: 35-spanish-teacher-deep-dive.md ===
# 35 - Spanish Teacher (Deep Dive: The Subjunctive State of Mind)

The subjunctive is the most difficult concept for English speakers to master in Spanish because it is not merely a set of conjugations; it is a psychological state. It represents how the speaker *feels* about the action, rather than whether the action is objectively happening.

## The Indicative vs. The Subjunctive
- **Indicative:** The world of facts, declarations, certainty, and objective reality.
- **Subjunctive:** The world of emotions, doubts, desires, hypotheticals, and subjective reactions.

### Example 1: Declaration vs. Emotion
- **Indicative:** *Sé que él viene.* (I know that he is coming.) -> Declaration of a fact.
- **Subjunctive:** *Me alegro de que él venga.* (I am happy that he is coming.) -> The fact that he is coming is secondary to my emotional reaction to it.

### Example 2: Certainty vs. Doubt
- **Indicative:** *Creo que es verdad.* (I believe it is true.) -> Certainty in the speaker's mind.
- **Subjunctive:** *No creo que sea verdad.* (I don't believe it is true.) -> Introduction of doubt.

## The WEIRDO Framework
Use this acronym to remember when to trigger the subjunctive in noun clauses (clauses starting with "que").

### W - Wishes and Desires
Verbs: querer, desear, preferir, esperar, necesitar.
- *Quiero que tú estudies.* (I want you to study.)

### E - Emotions
Verbs: alegrarse, enojar, sentir, temer, gustar, encantar.
- *Siento que estés enfermo.* (I am sorry that you are sick.)

### I - Impersonal Expressions
Phrases: es necesario, es importante, es posible, es probable, es ridículo.
- *Es importante que lleguemos a tiempo.* (It is important that we arrive on time.)

### R - Recommendations and Requests
Verbs: recomendar, sugerir, aconsejar, pedir, mandar.
- *Te sugiero que leas este libro.* (I suggest that you read this book.)

### D - Doubt and Denial
Verbs: dudar, negar, no creer, no pensar.
- *Dudo que llueva mañana.* (I doubt that it will rain tomorrow.)

### O - Ojalá
An Arabic loanword meaning "God willing" or "I hope". Always triggers the subjunctive.
- *¡Ojalá que ganemos el partido!* (I hope we win the game!)

## Adjective Clauses: The Unknown Antecedent
The subjunctive is used when describing something that may not exist or is unknown to the speaker.
- **Indicative (Known):** *Tengo una secretaria que habla francés.* (I have a secretary who speaks French. -> I know her, she exists.)
- **Subjunctive (Unknown):** *Busco una secretaria que hable francés.* (I am looking for a secretary who speaks French. -> She may or may not exist, I haven't found her yet.)

## === FILE: 35-spanish-teacher-security-audit.md ===
# 35 - Spanish Teacher (Cultural Sensitivity & Appropriateness Audit)

In language learning, "security" translates to cultural competence, avoiding offensive language, and understanding regional sensitivities.

## 1. The "Coger" Warning (Latin America vs. Spain)
- **Spain:** "Coger" is a completely standard verb meaning "to take" or "to catch" (e.g., coger el autobús).
- **Latin America (especially Mexico and Argentina):** "Coger" is highly vulgar slang for sexual intercourse.
- **Audit Fix:** Teach learners to use "tomar" or "agarrar" when traveling in Latin America.

## 2. The "Concha" Warning (Spain vs. South America)
- **Spain:** "Concha" means shell (seashell) and is a common name (short for Concepción).
- **Argentina/Uruguay/Chile:** "Concha" is vulgar slang for female genitalia.
- **Audit Fix:** Use "caracol" for shell in the Southern Cone.

## 3. Formality and "Usted"
- **Audit Risk:** Using "tú" with an elderly person, a boss, or a stranger in formal cultures (like Colombia or Mexico) can be perceived as highly disrespectful.
- **Audit Fix:** Always default to "usted" in professional settings or with elders until invited to use "tú" (the verb is "tutear").
- **Exception:** In Spain, "tú" is used much more freely, even with strangers and teachers.

## 4. Racial and Descriptive Terminology
- **Audit Risk:** Direct translation of English racial terms can be problematic, while Spanish terms that sound offensive in English are often terms of endearment.
- **Example:** "Gordo/a" (fat) or "Flaco/a" (skinny) are commonly used affectionately among friends and family in Latin America, without the negative connotation they carry in English.
- **Example:** "Negro/a" or "Negrito/a" is frequently used as a term of endearment for partners or friends, regardless of actual race, and is not inherently a racial slur in Spanish.

## 5. The "Vosotros" Exclusion
- **Audit Risk:** Teaching only Latin American Spanish and ignoring "vosotros" leaves learners confused when watching Spanish media (like La Casa de Papel).
- **Audit Fix:** Ensure receptive understanding of "vosotros" conjugations even if the learner chooses not to use them actively.

## === FILE: 35-spanish-teacher-specialist.md ===
# 35 - Spanish Teacher Supreme: Complete A1-C2 Master Guide

> This document is a comprehensive, self-contained Spanish language course covering all CEFR levels from absolute beginner (A1) to mastery (C2). It includes pronunciation, grammar, conjugation tables for every tense, vocabulary, conversation patterns, cultural context, and exercises. Use this as the definitive reference for learning, teaching, or building Spanish language AI systems.

---

## Part 1: Foundation (A1 - Absolute Beginner)

### 1.1 The Spanish Alphabet and Pronunciation

The Spanish alphabet contains 27 letters. Spanish is a phonetic language, meaning words are pronounced exactly as they are written. Once you learn the pronunciation rules, you can read any word aloud correctly.

**Vowels (always consistent, never change):**

| Letter | Sound | Example | Translation |
|--------|-------|---------|-------------|
| A | "ah" (like "father") | casa | house |
| E | "eh" (like "bet") | mesa | table |
| I | "ee" (like "see") | libro | book |
| O | "oh" (like "go") | sol | sun |
| U | "oo" (like "moon") | luna | moon |

**Consonants with special rules:**

| Letter/Combo | Rule | Example | Pronunciation |
|-------------|------|---------|---------------|
| C + a/o/u | /k/ sound | casa, comer, cubo | KAH-sah, koh-MEHR |
| C + e/i | /s/ (LatAm) or /th/ (Spain) | cielo, cena | see-EH-loh, SEH-nah |
| G + a/o/u | /g/ sound | gato, goma | GAH-toh |
| G + e/i | /h/ harsh sound | gente, girar | HEN-teh |
| GU + e/i | /g/ sound (u is silent) | guerra, guitarra | GEH-rrah |
| H | always silent | hola, hacer | OH-lah, ah-SEHR |
| J | harsh /h/ sound | jugar, jefe | hoo-GAHR |
| LL | /y/ sound (most regions) | llamar, calle | yah-MAHR |
| N with tilde | /ny/ sound (like "canyon") | nino, ano | NEE-nyoh |
| QU | /k/ sound (u is silent) | queso, quien | KEH-soh |
| R (initial) | rolled/trilled | rosa, raton | RROH-sah |
| RR | strongly rolled | perro, carro | PEH-rroh |
| V | same as B in most dialects | vino, vaca | BEE-noh |
| Z | /s/ (LatAm) or /th/ (Spain) | zapato, azul | sah-PAH-toh |

**Stress rules (accentuation):**
1. Words ending in a vowel, -n, or -s: stress falls on the second-to-last syllable (e.g., ca-SA, ha-BLAN).
2. Words ending in any other consonant: stress falls on the last syllable (e.g., ha-BLAR, ciu-DAD).
3. If a word breaks these rules, a written accent (tilde) marks the stressed syllable (e.g., ca-FE, te-LE-fo-no, MU-si-ca).

### 1.2 Greetings, Introductions, and Basic Phrases

**Greetings by time of day:**
- Buenos dias (Good morning) - used until approximately noon
- Buenas tardes (Good afternoon) - used from noon until sunset
- Buenas noches (Good evening/night) - used after sunset

**Meeting someone:**
- Hola, me llamo [nombre]. (Hello, my name is [name].)
- Como te llamas? (What is your name? - informal)
- Como se llama usted? (What is your name? - formal)
- Mucho gusto. / Encantado/a. (Nice to meet you.)
- De donde eres? (Where are you from? - informal)
- Soy de [pais/ciudad]. (I am from [country/city].)

**Essential survival phrases:**
- Por favor (Please)
- Gracias / Muchas gracias (Thank you / Thank you very much)
- De nada (You're welcome)
- Lo siento (I'm sorry)
- Disculpe / Perdon (Excuse me / Pardon)
- No entiendo (I don't understand)
- Puede repetir, por favor? (Can you repeat, please?)
- Habla ingles? (Do you speak English?)
- Hablo un poco de espanol. (I speak a little Spanish.)
- Cuanto cuesta? (How much does it cost?)
- Donde esta el bano? (Where is the bathroom?)
- La cuenta, por favor. (The check, please.)

### 1.3 Nouns: Gender and Number

Every Spanish noun is either masculine or feminine. There is no neutral gender (except for the abstract "lo").

**Gender identification rules:**

| Ending | Gender | Examples | Exceptions |
|--------|--------|----------|------------|
| -o | Masculine | el libro, el gato, el vaso | la mano (hand), la foto, la radio |
| -a | Feminine | la casa, la mesa, la silla | el dia (day), el mapa, el problema |
| -cion/-sion | Feminine | la cancion, la television | (none) |
| -dad/-tad | Feminine | la ciudad, la libertad | (none) |
| -ma | Masculine (Greek origin) | el problema, el sistema, el clima | la cama (bed), la llama |
| -ista | Both (context) | el/la artista, el/la dentista | (none) |

**Pluralization rules:**
- Noun ends in a vowel: add -s (libro to libros, casa to casas).
- Noun ends in a consonant: add -es (ciudad to ciudades, color to colores).
- Noun ends in -z: change to -ces (lapiz to lapices, vez to veces).

**Articles:**

| Type | Masculine Singular | Feminine Singular | Masculine Plural | Feminine Plural |
|------|-------------------|------------------|-----------------|----------------|
| Definite (the) | el | la | los | las |
| Indefinite (a/some) | un | una | unos | unas |

### 1.4 Subject Pronouns and Verb "Ser" (To Be - Permanent)

**Subject pronouns:**

| Person | Singular | Plural |
|--------|----------|--------|
| 1st | yo (I) | nosotros/nosotras (we) |
| 2nd informal | tu (you) | vosotros/vosotras (you all - Spain) |
| 2nd formal | usted (Ud.) | ustedes (Uds.) |
| 3rd | el/ella (he/she) | ellos/ellas (they) |

**Ser - Present Tense (identity, origin, profession, time, material, possession):**

| Pronoun | Conjugation | Example |
|---------|-------------|---------|
| Yo | soy | Yo soy profesor. (I am a teacher.) |
| Tu | eres | Tu eres inteligente. (You are intelligent.) |
| El/Ella/Ud. | es | Ella es de Colombia. (She is from Colombia.) |
| Nosotros/as | somos | Nosotros somos amigos. (We are friends.) |
| Vosotros/as | sois | Vosotros sois espanoles. (You all are Spanish.) |
| Ellos/Ellas/Uds. | son | Ellos son medicos. (They are doctors.) |

**Uses of Ser (mnemonic: DOCTOR):**
- **D**escription (inherent qualities): El coche es rojo. (The car is red.)
- **O**ccupation: Ella es abogada. (She is a lawyer.)
- **C**haracteristic: El es alto. (He is tall.)
- **T**ime/Date: Son las tres. (It is three o'clock.) / Hoy es lunes. (Today is Monday.)
- **O**rigin: Somos de Brasil. (We are from Brazil.)
- **R**elationship: Ella es mi hermana. (She is my sister.)

### 1.5 Verb "Estar" (To Be - Temporary/Location)

**Estar - Present Tense:**

| Pronoun | Conjugation | Example |
|---------|-------------|---------|
| Yo | estoy | Estoy cansado. (I am tired.) |
| Tu | estas | Estas bien? (Are you okay?) |
| El/Ella/Ud. | esta | Ella esta en la oficina. (She is at the office.) |
| Nosotros/as | estamos | Estamos contentos. (We are happy.) |
| Vosotros/as | estais | Estais listos? (Are you all ready?) |
| Ellos/Ellas/Uds. | estan | Estan en el parque. (They are in the park.) |

**Uses of Estar (mnemonic: PLACE):**
- **P**osition/Posture: Estoy sentado. (I am seated.)
- **L**ocation: El banco esta en la esquina. (The bank is on the corner.)
- **A**ction (progressive): Estoy comiendo. (I am eating.)
- **C**ondition: La puerta esta abierta. (The door is open.)
- **E**motion: Estoy feliz. (I am happy.)

### 1.6 Regular Verbs: Present Indicative

Spanish verbs are categorized by their infinitive endings: -AR, -ER, -IR.

**-AR Verbs (the largest group):**

| Pronoun | Hablar (speak) | Trabajar (work) | Estudiar (study) |
|---------|---------------|-----------------|------------------|
| Yo | hablo | trabajo | estudio |
| Tu | hablas | trabajas | estudias |
| El/Ella/Ud. | habla | trabaja | estudia |
| Nosotros | hablamos | trabajamos | estudiamos |
| Vosotros | hablais | trabajais | estudiais |
| Ellos/Uds. | hablan | trabajan | estudian |

**Common -AR verbs:** amar (love), bailar (dance), buscar (search), caminar (walk), cantar (sing), cenar (dine), cocinar (cook), comprar (buy), descansar (rest), ensenar (teach), escuchar (listen), esperar (wait/hope), lavar (wash), limpiar (clean), llamar (call), llegar (arrive), llevar (carry/wear), mirar (look), nadar (swim), necesitar (need), pagar (pay), pasar (pass/spend time), practicar (practice), preguntar (ask), preparar (prepare), terminar (finish), tomar (take/drink), viajar (travel), visitar (visit).

**-ER Verbs:**

| Pronoun | Comer (eat) | Beber (drink) | Leer (read) |
|---------|------------|--------------|-------------|
| Yo | como | bebo | leo |
| Tu | comes | bebes | lees |
| El/Ella/Ud. | come | bebe | lee |
| Nosotros | comemos | bebemos | leemos |
| Vosotros | comeis | bebeis | leeis |
| Ellos/Uds. | comen | beben | leen |

**Common -ER verbs:** aprender (learn), barrer (sweep), comprender (understand), correr (run), creer (believe), deber (must/owe), meter (put in), prometer (promise), responder (respond), romper (break), vender (sell).

**-IR Verbs:**

| Pronoun | Vivir (live) | Escribir (write) | Abrir (open) |
|---------|------------|-----------------|-------------|
| Yo | vivo | escribo | abro |
| Tu | vives | escribes | abres |
| El/Ella/Ud. | vive | escribe | abre |
| Nosotros | vivimos | escribimos | abrimos |
| Vosotros | vivis | escribis | abris |
| Ellos/Uds. | viven | escriben | abren |

**Common -IR verbs:** asistir (attend), compartir (share), decidir (decide), describir (describe), discutir (discuss/argue), existir (exist), insistir (insist), ocurrir (occur), permitir (permit), recibir (receive), subir (go up/upload), sufrir (suffer).

### 1.7 Irregular Verbs: Present Indicative (Most Common)

| Verb | Yo | Tu | El/Ella | Nosotros | Vosotros | Ellos |
|------|----|----|---------|----------|----------|-------|
| Ir (go) | voy | vas | va | vamos | vais | van |
| Tener (have) | tengo | tienes | tiene | tenemos | teneis | tienen |
| Hacer (do/make) | hago | haces | hace | hacemos | haceis | hacen |
| Decir (say) | digo | dices | dice | decimos | decis | dicen |
| Poder (can) | puedo | puedes | puede | podemos | podeis | pueden |
| Querer (want) | quiero | quieres | quiere | queremos | quereis | quieren |
| Saber (know) | se | sabes | sabe | sabemos | sabeis | saben |
| Conocer (know) | conozco | conoces | conoce | conocemos | conoceis | conocen |
| Venir (come) | vengo | vienes | viene | venimos | venis | vienen |
| Salir (leave) | salgo | sales | sale | salimos | salis | salen |
| Poner (put) | pongo | pones | pone | ponemos | poneis | ponen |
| Dar (give) | doy | das | da | damos | dais | dan |
| Ver (see) | veo | ves | ve | vemos | veis | ven |
| Oir (hear) | oigo | oyes | oye | oimos | ois | oyen |
| Traer (bring) | traigo | traes | trae | traemos | traeis | traen |

### 1.8 Numbers, Time, Days, Months

**Numbers 0-1000:**
0-cero, 1-uno, 2-dos, 3-tres, 4-cuatro, 5-cinco, 6-seis, 7-siete, 8-ocho, 9-nueve, 10-diez, 11-once, 12-doce, 13-trece, 14-catorce, 15-quince, 16-dieciseis, 17-diecisiete, 18-dieciocho, 19-diecinueve, 20-veinte, 21-veintiuno, 22-veintidos, 30-treinta, 31-treinta y uno, 40-cuarenta, 50-cincuenta, 60-sesenta, 70-setenta, 80-ochenta, 90-noventa, 100-cien/ciento, 200-doscientos, 300-trescientos, 400-cuatrocientos, 500-quinientos, 600-seiscientos, 700-setecientos, 800-ochocientos, 900-novecientos, 1000-mil.

**Ordinal numbers:** primero (1st), segundo (2nd), tercero (3rd), cuarto (4th), quinto (5th), sexto (6th), septimo (7th), octavo (8th), noveno (9th), decimo (10th).

**Telling time:**
- Que hora es? (What time is it?)
- Es la una. (It is 1:00.) - singular because "una" = one hour
- Son las dos / tres / cuatro... (It is 2:00 / 3:00 / 4:00...)
- Son las tres y cuarto. (It is 3:15.)
- Son las tres y media. (It is 3:30.)
- Son las cuatro menos cuarto. (It is 3:45 / a quarter to four.)
- de la manana (a.m.), de la tarde (p.m. afternoon), de la noche (p.m. evening)

**Days of the week (not capitalized in Spanish):**
lunes (Monday), martes (Tuesday), miercoles (Wednesday), jueves (Thursday), viernes (Friday), sabado (Saturday), domingo (Sunday).

**Months (not capitalized):**
enero, febrero, marzo, abril, mayo, junio, julio, agosto, septiembre, octubre, noviembre, diciembre.

**Seasons:** la primavera (spring), el verano (summer), el otono (autumn), el invierno (winter).

---

## Part 2: Elementary (A2)

### 2.1 Stem-Changing Verbs (Boot Verbs)

These verbs change their stem vowel in all forms except nosotros and vosotros, creating a "boot" pattern in conjugation charts.

**E to IE verbs:**

| Verb | Yo | Tu | El/Ella | Nosotros | Ellos |
|------|----|----|---------|----------|-------|
| Pensar (think) | pienso | piensas | piensa | pensamos | piensan |
| Empezar (begin) | empiezo | empiezas | empieza | empezamos | empiezan |
| Entender (understand) | entiendo | entiendes | entiende | entendemos | entienden |
| Preferir (prefer) | prefiero | prefieres | prefiere | preferimos | prefieren |
| Cerrar (close) | cierro | cierras | cierra | cerramos | cierran |
| Perder (lose) | pierdo | pierdes | pierde | perdemos | pierden |
| Sentir (feel) | siento | sientes | siente | sentimos | sienten |

**O to UE verbs:**

| Verb | Yo | Tu | El/Ella | Nosotros | Ellos |
|------|----|----|---------|----------|-------|
| Poder (can) | puedo | puedes | puede | podemos | pueden |
| Dormir (sleep) | duermo | duermes | duerme | dormimos | duermen |
| Volver (return) | vuelvo | vuelves | vuelve | volvemos | vuelven |
| Encontrar (find) | encuentro | encuentras | encuentra | encontramos | encuentran |
| Contar (count/tell) | cuento | cuentas | cuenta | contamos | cuentan |
| Recordar (remember) | recuerdo | recuerdas | recuerda | recordamos | recuerdan |
| Morir (die) | muero | mueres | muere | morimos | mueren |

**E to I verbs (only -IR verbs):**

| Verb | Yo | Tu | El/Ella | Nosotros | Ellos |
|------|----|----|---------|----------|-------|
| Pedir (ask for) | pido | pides | pide | pedimos | piden |
| Servir (serve) | sirvo | sirves | sirve | servimos | sirven |
| Repetir (repeat) | repito | repites | repite | repetimos | repiten |
| Seguir (follow) | sigo | sigues | sigue | seguimos | siguen |
| Vestirse (dress) | me visto | te vistes | se viste | nos vestimos | se visten |

### 2.2 Reflexive Verbs (Daily Routine)

Reflexive verbs indicate that the subject performs and receives the action. They use reflexive pronouns: me, te, se, nos, os, se.

**Levantarse (to get up):**
Me levanto, te levantas, se levanta, nos levantamos, os levantais, se levantan.

**Common reflexive verbs for daily routine:**
- despertarse (e to ie) - to wake up: Me despierto a las siete.
- levantarse - to get up: Me levanto inmediatamente.
- ducharse - to shower: Me ducho con agua caliente.
- banarse - to bathe: Me bano por la noche.
- lavarse (la cara/las manos/los dientes) - to wash: Me lavo los dientes.
- peinarse - to comb one's hair: Me peino frente al espejo.
- vestirse (e to i) - to get dressed: Me visto rapidamente.
- maquillarse - to put on makeup: Ella se maquilla.
- afeitarse - to shave: El se afeita cada manana.
- sentarse (e to ie) - to sit down: Me siento en la silla.
- acostarse (o to ue) - to go to bed: Me acuesto a las once.
- dormirse (o to ue) - to fall asleep: Me duermo rapido.
- irse - to leave: Me voy a las ocho.
- ponerse - to put on (clothing): Me pongo el abrigo.
- quitarse - to take off: Me quito los zapatos.

### 2.3 The Preterite Tense (Completed Past Actions)

The preterite is used for actions that were completed at a specific point in the past.

**Regular -AR (Hablar):**

| Pronoun | Ending | Conjugation |
|---------|--------|-------------|
| Yo | -e | hable |
| Tu | -aste | hablaste |
| El/Ella/Ud. | -o | hablo |
| Nosotros | -amos | hablamos |
| Vosotros | -asteis | hablasteis |
| Ellos/Uds. | -aron | hablaron |

**Regular -ER/-IR (Comer/Vivir):**

| Pronoun | Ending | Comer | Vivir |
|---------|--------|-------|-------|
| Yo | -i | comi | vivi |
| Tu | -iste | comiste | viviste |
| El/Ella/Ud. | -io | comio | vivio |
| Nosotros | -imos | comimos | vivimos |
| Vosotros | -isteis | comisteis | vivisteis |
| Ellos/Uds. | -ieron | comieron | vivieron |

**Irregular Preterite (the "big 8" - no accents on yo/el forms):**

| Verb | Stem | Yo | Tu | El | Nosotros | Ellos |
|------|------|----|----|-----|----------|-------|
| Tener | tuv- | tuve | tuviste | tuvo | tuvimos | tuvieron |
| Estar | estuv- | estuve | estuviste | estuvo | estuvimos | estuvieron |
| Poder | pud- | pude | pudiste | pudo | pudimos | pudieron |
| Poner | pus- | puse | pusiste | puso | pusimos | pusieron |
| Saber | sup- | supe | supiste | supo | supimos | supieron |
| Hacer | hic-/hiz- | hice | hiciste | hizo | hicimos | hicieron |
| Venir | vin- | vine | viniste | vino | vinimos | vinieron |
| Querer | quis- | quise | quisiste | quiso | quisimos | quisieron |

**Completely irregular:**
- Ir/Ser: fui, fuiste, fue, fuimos, fuisteis, fueron (same conjugation for both verbs!)
- Dar: di, diste, dio, dimos, disteis, dieron
- Decir: dije, dijiste, dijo, dijimos, dijisteis, dijeron
- Traer: traje, trajiste, trajo, trajimos, trajisteis, trajeron
- Conducir: conduje, condujiste, condujo, condujimos, condujisteis, condujeron

**Spelling changes in the preterite (yo form only):**
- -car verbs: c to qu (buscar: busque)
- -gar verbs: g to gu (llegar: llegue)
- -zar verbs: z to c (empezar: empece)

### 2.4 The Imperfect Tense (Ongoing/Habitual Past)

The imperfect describes ongoing states, habitual actions, or background descriptions in the past.

**Regular -AR (Hablar):**

| Pronoun | Ending | Conjugation |
|---------|--------|-------------|
| Yo | -aba | hablaba |
| Tu | -abas | hablabas |
| El/Ella/Ud. | -aba | hablaba |
| Nosotros | -abamos | hablabamos |
| Vosotros | -abais | hablabais |
| Ellos/Uds. | -aban | hablaban |

**Regular -ER/-IR (Comer/Vivir):**

| Pronoun | Ending | Comer | Vivir |
|---------|--------|-------|-------|
| Yo | -ia | comia | vivia |
| Tu | -ias | comias | vivias |
| El/Ella/Ud. | -ia | comia | vivia |
| Nosotros | -iamos | comiamos | viviamos |
| Vosotros | -iais | comiais | viviais |
| Ellos/Uds. | -ian | comian | vivian |

**Only 3 irregular verbs in the imperfect:**
- Ir: iba, ibas, iba, ibamos, ibais, iban
- Ser: era, eras, era, eramos, erais, eran
- Ver: veia, veias, veia, veiamos, veiais, veian

**Preterite vs. Imperfect decision guide:**

| Use Preterite when... | Use Imperfect when... |
|----------------------|----------------------|
| Action completed at a specific time | Action was ongoing (no clear end) |
| Action happened once | Action was habitual/repeated |
| A sequence of completed events | Setting the scene (weather, time, age) |
| An interrupting action | The action being interrupted |
| Beginning or end of an action | Physical/emotional descriptions |

*Example combining both:* "Yo caminaba (imperfect - ongoing) por el parque cuando vi (preterite - interruption) a mi amigo."

**Time markers for preterite:** ayer, anoche, la semana pasada, el ano pasado, una vez, de repente.
**Time markers for imperfect:** siempre, todos los dias, a menudo, frecuentemente, cuando era nino/a, generalmente.

### 2.5 Direct and Indirect Object Pronouns

**Direct Object Pronouns (replace the thing/person receiving the action):**

| Person | Singular | Plural |
|--------|----------|--------|
| 1st | me (me) | nos (us) |
| 2nd | te (you) | os (you all) |
| 3rd | lo/la (him/her/it/you formal) | los/las (them/you all formal) |

*Example:* Ves el libro? Si, lo veo. (Do you see the book? Yes, I see it.)

**Indirect Object Pronouns (replace the person to/for whom the action is done):**

| Person | Singular | Plural |
|--------|----------|--------|
| 1st | me (to me) | nos (to us) |
| 2nd | te (to you) | os (to you all) |
| 3rd | le (to him/her/you formal) | les (to them/you all formal) |

*Example:* Doy el libro a Maria. Le doy el libro. (I give the book to Maria. I give her the book.)

**Double object pronouns (IOP always comes first):**
When both appear together, the indirect comes before the direct: Me lo da. (He gives it to me.)
When le/les precedes lo/la/los/las, change le/les to "se": Le lo doy becomes Se lo doy.

**Pronoun placement rules:**
- Before conjugated verbs: Lo veo. (I see it.)
- Attached to infinitives: Quiero verlo. OR Lo quiero ver.
- Attached to gerunds: Estoy haciendolo. OR Lo estoy haciendo.
- Attached to affirmative commands: Dimelo. (Tell it to me.)
- Before negative commands: No me lo digas. (Don't tell it to me.)

### 2.6 Gustar and Similar Verbs

"Gustar" literally means "to please" - the thing you like is the subject.

**Structure:** Indirect Object Pronoun + gusta/gustan + subject

| English | Spanish |
|---------|---------|
| I like the book | Me gusta el libro (The book pleases me) |
| I like the books | Me gustan los libros (The books please me) |
| She likes to dance | Le gusta bailar (Dancing pleases her) |
| We like the movies | Nos gustan las peliculas |
| They like music | Les gusta la musica |

**Similar verbs that follow the same pattern:**
- encantar (to love/enchant): Me encanta la musica.
- importar (to matter): No me importa.
- interesar (to interest): Te interesa la historia?
- molestar (to bother): Me molesta el ruido.
- doler (o to ue) (to hurt): Me duele la cabeza.
- faltar (to lack/need): Me faltan dos dolares.
- parecer (to seem): Me parece bien.
- quedar (to remain/fit): No me queda dinero. / Me queda bien la camisa.
- fascinar (to fascinate): Nos fascinan los idiomas.
- preocupar (to worry): Le preocupa el examen.

---

## Part 3: Intermediate (B1)

### 3.1 The Future Tense

**Simple Future (add endings to the full infinitive):**

Endings (same for -AR, -ER, -IR): -e, -as, -a, -emos, -eis, -an.

| Pronoun | Hablar | Comer | Vivir |
|---------|--------|-------|-------|
| Yo | hablare | comere | vivire |
| Tu | hablaras | comeras | viviras |
| El/Ella | hablara | comera | vivira |
| Nosotros | hablaremos | comeremos | viviremos |
| Vosotros | hablareis | comereis | vivireis |
| Ellos | hablaran | comeran | viviran |

**Irregular future stems (same endings):**

| Verb | Irregular Stem | Example (yo) |
|------|---------------|--------------|
| Tener | tendr- | tendre |
| Venir | vendr- | vendre |
| Poner | pondr- | pondre |
| Salir | saldr- | saldre |
| Poder | podr- | podre |
| Saber | sabr- | sabre |
| Hacer | har- | hare |
| Decir | dir- | dire |
| Querer | querr- | querre |
| Haber | habr- | habra |
| Valer | valdr- | valdre |
| Caber | cabr- | cabre |

**Uses of the future tense:**
- Future actions: Manana estudiare. (Tomorrow I will study.)
- Predictions: Llovera esta noche. (It will rain tonight.)
- Probability in the present: Seran las tres. (It's probably three o'clock.)
- Promises: Te llamare manana. (I will call you tomorrow.)

**Informal future (ir + a + infinitive):**
- Voy a estudiar. (I am going to study.) - more common in spoken Spanish.

### 3.2 The Conditional Tense

Expresses what "would" happen. Uses the same irregular stems as the future.

Endings (same for all verbs): -ia, -ias, -ia, -iamos, -iais, -ian.

| Pronoun | Hablar | Tener | Hacer |
|---------|--------|-------|-------|
| Yo | hablaria | tendria | haria |
| Tu | hablarias | tendrias | harias |
| El/Ella | hablaria | tendria | haria |
| Nosotros | hablariamos | tendriamos | hariamos |
| Vosotros | hablariais | tendriais | hariais |
| Ellos | hablarian | tendrian | harian |

**Uses of the conditional:**
- Polite requests: Podrias ayudarme? (Could you help me?)
- Hypothetical situations: Con mas dinero, viajaria mas. (With more money, I would travel more.)
- Future in the past: Dijo que vendria. (He said he would come.)
- Probability in the past: Serian las tres cuando llego. (It was probably three when he arrived.)
- Advice: Yo que tu, estudiaria mas. (If I were you, I would study more.)

### 3.3 Por vs. Para (Complete Guide)

**POR (mnemonic: DEEMMRT):**
- **D**uration: Estudie por tres horas. (I studied for three hours.)
- **E**xchange: Pague $50 por el libro. (I paid $50 for the book.)
- **E**motion/Reason: Lo hago por amor. (I do it for/out of love.)
- **M**ovement through: Caminamos por el parque. (We walked through the park.)
- **M**eans of communication/transport: Hablamos por telefono. (We spoke by phone.)
- **R**eplacement (on behalf of): Trabajo por mi hermano hoy. (I'm working for my brother today.)
- **T**imes (multiplication): Dos por tres son seis. (Two times three is six.)

Additional por uses:
- Per: Tres veces por semana. (Three times per week.)
- Approximate location: Vive por aqui. (He lives around here.)
- Passive agent: El libro fue escrito por Cervantes. (The book was written by Cervantes.)
- Gratitude/apology: Gracias por todo. (Thanks for everything.)

**PARA (mnemonic: PERFECT):**
- **P**urpose/Goal: Estudio para aprender. (I study in order to learn.)
- **E**mployee (recipient): Este regalo es para ti. (This gift is for you.)
- **R**eadiness/Deadline: La tarea es para manana. (The homework is for/due tomorrow.)
- **F**uture destination: Salgo para Madrid. (I'm leaving for Madrid.)
- **E**ffect (in order to): Para ser feliz, necesitas amigos. (In order to be happy, you need friends.)
- **C**omparison: Para un nino, habla muy bien. (For a child, he speaks very well.)
- **T**ype/Use: Es una taza para cafe. (It's a cup for coffee.)

Additional para uses:
- Opinion: Para mi, es importante. (For me / In my opinion, it's important.)
- Employment: Trabajo para Google. (I work for Google.)

### 3.4 Commands (Imperative Mood)

**Informal affirmative (tu) commands - use the el/ella present indicative form:**
habla (speak), come (eat), escribe (write), piensa (think), vuelve (return).

**Irregular tu commands (8 verbs - mnemonic: Ven Di Sal Haz Ten Ve Pon Se):**
ven (venir), di (decir), sal (salir), haz (hacer), ten (tener), ve (ir), pon (poner), se (ser).

**Informal negative (tu) commands - use the tu present subjunctive form:**
no hables, no comas, no escribas, no vengas, no digas, no salgas, no hagas.

**Formal (usted/ustedes) commands - use the present subjunctive:**
hable/hablen, coma/coman, escriba/escriban, venga/vengan, diga/digan.

**Nosotros commands (Let's...):**
hablemos (let's speak), comamos (let's eat), escribamos (let's write).
Irregular: vamos (let's go) - but "no vayamos" for negative.

**Vosotros commands:**
Affirmative: change -r of infinitive to -d (hablar to hablad, comer to comed, vivir to vivid).
Negative: no hableis, no comais, no escribais.

**Pronoun placement with commands:**
- Affirmative: attach to the end (add accent if needed): Dimelo. (Tell it to me.) / Sientese. (Sit down.)
- Negative: place before the verb: No me lo digas. (Don't tell it to me.) / No se siente. (Don't sit down.)

### 3.5 The Present Progressive (Gerund)

**Formation:** estar + gerund (-ando for -AR, -iendo for -ER/-IR)

| Verb Type | Gerund | Example |
|-----------|--------|---------|
| -AR (hablar) | hablando | Estoy hablando. (I am speaking.) |
| -ER (comer) | comiendo | Estamos comiendo. (We are eating.) |
| -IR (vivir) | viviendo | Estan viviendo aqui. (They are living here.) |

**Irregular gerunds:**
- Stem-changing -IR verbs: e to i (decir: diciendo, pedir: pidiendo, servir: sirviendo)
- Stem-changing -IR verbs: o to u (dormir: durmiendo, morir: muriendo)
- Verbs with stems ending in vowel: -yendo (leer: leyendo, oir: oyendo, traer: trayendo)
- Ir: yendo

---

## Part 4: Upper Intermediate (B2)

### 4.1 The Present Subjunctive

**Formation:** Take the "yo" present indicative, drop the -o, add opposite endings.

| Type | -AR verbs get | -ER/-IR verbs get |
|------|--------------|-------------------|
| Yo | -e | -a |
| Tu | -es | -as |
| El/Ella | -e | -a |
| Nosotros | -emos | -amos |
| Vosotros | -eis | -ais |
| Ellos | -en | -an |

**Examples:**

| Verb | Yo Indicative | Subjunctive (yo/tu/el) |
|------|--------------|------------------------|
| Hablar | hablo to habl- | hable, hables, hable |
| Comer | como to com- | coma, comas, coma |
| Tener | tengo to teng- | tenga, tengas, tenga |
| Hacer | hago to hag- | haga, hagas, haga |
| Decir | digo to dig- | diga, digas, diga |
| Conocer | conozco to conozc- | conozca, conozcas, conozca |
| Poner | pongo to pong- | ponga, pongas, ponga |
| Salir | salgo to salg- | salga, salgas, salga |
| Venir | vengo to veng- | venga, vengas, venga |
| Traer | traigo to traig- | traiga, traigas, traiga |

**Irregular subjunctive (DISHES):**
- Dar: de, des, de, demos, deis, den
- Ir: vaya, vayas, vaya, vayamos, vayais, vayan
- Ser: sea, seas, sea, seamos, seais, sean
- Haber: haya, hayas, haya, hayamos, hayais, hayan
- Estar: este, estes, este, estemos, esteis, esten
- Saber: sepa, sepas, sepa, sepamos, sepais, sepan

**WEIRDO triggers (when to use subjunctive):**
- **W**ishes/Will: Quiero que vengas. (I want you to come.) / Espero que estes bien. (I hope you are well.)
- **E**motions: Me alegra que estes aqui. (I'm glad you're here.) / Siento que estes enfermo. (I'm sorry you're sick.)
- **I**mpersonal expressions: Es necesario que estudies. (It's necessary that you study.) / Es posible que llueva. (It's possible it will rain.)
- **R**ecommendations/Requests: Te sugiero que vayas. (I suggest you go.) / Te pido que me ayudes. (I ask you to help me.)
- **D**oubt/Denial: Dudo que sea verdad. (I doubt it's true.) / No creo que venga. (I don't think he'll come.)
- **O**jala: Ojala que llueva. (I hope it rains.) / Ojala pudiera ir. (I wish I could go.)

**Additional subjunctive triggers:**
- After conjunctions of time (when referring to future): Cuando llegues, llamame. (When you arrive, call me.)
- After "para que": Te lo digo para que sepas. (I tell you so that you know.)
- After "sin que": Salio sin que yo lo supiera. (He left without me knowing.)
- After "a menos que": Ire a menos que llueva. (I'll go unless it rains.)
- After "antes de que": Antes de que te vayas... (Before you leave...)
- Adjective clauses with unknown antecedent: Busco un apartamento que tenga balcon. (I'm looking for an apartment that has a balcony.)

### 4.2 The Imperfect Subjunctive

**Formation:** Take the ellos preterite form, drop -ron, add endings.

Two sets of endings exist (both are correct, -ra form is more common):

| Pronoun | -ra endings | -se endings |
|---------|------------|------------|
| Yo | -ra | -se |
| Tu | -ras | -ses |
| El/Ella | -ra | -se |
| Nosotros | -ramos (accent!) | -semos |
| Vosotros | -rais | -seis |
| Ellos | -ran | -sen |

**Examples:**

| Verb | Ellos Preterite | Imperfect Subjunctive (yo) |
|------|----------------|---------------------------|
| Hablar | hablaron to habla- | hablara |
| Comer | comieron to comie- | comiera |
| Tener | tuvieron to tuvie- | tuviera |
| Ir/Ser | fueron to fue- | fuera |
| Hacer | hicieron to hicie- | hiciera |
| Decir | dijeron to dije- | dijera |
| Poder | pudieron to pudie- | pudiera |
| Poner | pusieron to pusie- | pusiera |
| Saber | supieron to supie- | supiera |
| Querer | quisieron to quisie- | quisiera |

**When to use the imperfect subjunctive:**
- After past-tense main clauses: Queria que vinieras. (I wanted you to come.)
- Polite requests: Quisiera un cafe. (I would like a coffee.)
- Si clauses (hypothetical): Si tuviera dinero, viajaria. (If I had money, I would travel.)
- After "como si" (as if): Habla como si fuera experto. (He speaks as if he were an expert.)

### 4.3 Si Clauses (If Clauses)

| Type | Si clause | Result clause | Example |
|------|-----------|---------------|---------|
| Possible (present/future) | Si + present indicative | Future / present / command | Si llueve, no salgo. / Si estudias, aprobaras. |
| Hypothetical (present) | Si + imperfect subjunctive | Conditional | Si tuviera dinero, viajaria. (If I had money, I would travel.) |
| Impossible (past) | Si + pluperfect subjunctive | Conditional perfect | Si hubiera estudiado, habria aprobado. (If I had studied, I would have passed.) |

**Important:** NEVER use present subjunctive after "si" in conditional sentences.

**Mixed conditionals:**
- Si hubiera estudiado (past), ahora tendria (present conditional) un mejor trabajo. (If I had studied, I would now have a better job.)

### 4.4 Perfect Tenses (Compound Tenses with Haber)

**Haber conjugations + past participle (-ado for -AR, -ido for -ER/-IR):**

| Tense | Haber Form | Example (hablar/comer) |
|-------|-----------|------------------------|
| Present Perfect | he, has, ha, hemos, habeis, han | He hablado / He comido (I have spoken/eaten) |
| Past Perfect (Pluperfect) | habia, habias, habia, habiamos, habiais, habian | Habia hablado (I had spoken) |
| Future Perfect | habre, habras, habra, habremos, habreis, habran | Habre hablado (I will have spoken) |
| Conditional Perfect | habria, habrias, habria, habriamos, habriais, habrian | Habria hablado (I would have spoken) |
| Present Perfect Subjunctive | haya, hayas, haya, hayamos, hayais, hayan | Haya hablado (That I have spoken) |
| Pluperfect Subjunctive | hubiera, hubieras, hubiera, hubieramos, hubierais, hubieran | Hubiera hablado (That I had spoken) |

**Irregular past participles:**
abrir to abierto, cubrir to cubierto, decir to dicho, escribir to escrito, hacer to hecho, morir to muerto, poner to puesto, resolver to resuelto, romper to roto, ver to visto, volver to vuelto, imprimir to impreso, freir to frito, satisfacer to satisfecho.

**Uses of perfect tenses:**
- Present perfect: actions completed recently or with present relevance: He comido ya. (I have already eaten.)
- Pluperfect: actions completed before another past action: Cuando llegue, ya habian salido. (When I arrived, they had already left.)
- Future perfect: actions that will be completed by a future point: Para las cinco, habre terminado. (By five, I will have finished.)
- Conditional perfect: hypothetical completed actions: Habria ido, pero estaba enfermo. (I would have gone, but I was sick.)

---

## Part 5: Advanced (C1-C2)

### 5.1 The Passive Voice

**True passive (less common in speech):** Ser + past participle (agrees in gender/number).
- El libro fue escrito por Cervantes. (The book was written by Cervantes.)
- Las casas fueron construidas en 1990. (The houses were built in 1990.)
- La carta sera enviada manana. (The letter will be sent tomorrow.)

**Se passive (more natural in Spanish):**
- Se venden libros aqui. (Books are sold here.)
- Se habla espanol. (Spanish is spoken.)
- Se necesitan empleados. (Employees are needed.)

**Se impersonal (no specific subject):**
- Se dice que va a llover. (It is said it will rain.)
- Se puede fumar aqui? (Can one smoke here?)
- Se vive bien en esta ciudad. (One lives well in this city.)

**Estar + past participle (resultant state, not action):**
- La puerta esta cerrada. (The door is closed.) - describes current state
- La puerta fue cerrada por el guardia. (The door was closed by the guard.) - describes action

### 5.2 Relative Pronouns and Clauses

| Pronoun | Use | Example |
|---------|-----|---------|
| que | most common (that/which/who) | El hombre que vino es mi padre. |
| quien/quienes | after prepositions for people | La mujer con quien hable es doctora. |
| el/la/los/las que | specific one(s) that | El que llego primero gano. |
| el/la cual, los/las cuales | formal, after prepositions | La casa en la cual vivo es vieja. |
| lo que | what (abstract concept) | No entiendo lo que dices. |
| lo cual | which (referring to a whole clause) | Llego tarde, lo cual me molesto. |
| cuyo/cuya/cuyos/cuyas | whose (agrees with possessed noun) | El autor cuyo libro lei es famoso. |
| donde | where | La ciudad donde naci es pequena. |
| cuando | when (as relative) | El dia cuando nos conocimos. |
| como | how/the way | La manera como habla es elegante. |

### 5.3 Advanced Vocabulary: 500+ Essential Words by Category

**Emotions and States (50 words):**
alegria (joy), tristeza (sadness), enojo/enfado (anger), miedo (fear), verguenza (shame), orgullo (pride), celos (jealousy), esperanza (hope), ansiedad (anxiety), soledad (loneliness), ternura (tenderness), asombro (amazement), desprecio (contempt), gratitud (gratitude), culpa (guilt), nostalgia (nostalgia), alivio (relief), frustracion (frustration), entusiasmo (enthusiasm), indiferencia (indifference), compasion (compassion), rencor (resentment), euforia (euphoria), melancolia (melancholy), desconfianza (distrust), admiracion (admiration), hartazgo (fed-up feeling), arrepentimiento (regret), satisfaccion (satisfaction), inquietud (unease).

**Professional/Work (50 words):**
empresa (company), jefe/a (boss), empleado/a (employee), sueldo/salario (salary), reunion (meeting), plazo (deadline), meta/objetivo (goal), presupuesto (budget), factura (invoice), contrato (contract), despido (firing), ascenso (promotion), jubilacion (retirement), sindicato (union), huelga (strike), entrevista (interview), curriculum (resume), capacitacion (training), horario (schedule), sede (headquarters), sucursal (branch), socio (partner), accionista (shareholder), ganancias (profits), perdidas (losses), ingresos (income), gastos (expenses), impuestos (taxes), nomina (payroll), prestaciones (benefits).

**Technology (50 words):**
pantalla (screen), teclado (keyboard), raton (mouse), contrasena (password), enlace (link), red (network), almacenamiento (storage), aplicacion (app), actualizacion (update), descargar (download), subir/cargar (upload), copia de seguridad (backup), inteligencia artificial (AI), base de datos (database), servidor (server), nube (cloud), algoritmo (algorithm), programacion (programming), codigo fuente (source code), depurar (debug), interfaz (interface), navegador (browser), buscador (search engine), disco duro (hard drive), memoria RAM (RAM), procesador (processor), virus informatico (computer virus), cortafuegos (firewall), cifrado (encryption), banda ancha (broadband).

**Health and Medicine (50 words):**
enfermedad (illness), sintoma (symptom), receta (prescription), pastilla (pill), cirugia (surgery), herida (wound), fiebre (fever), tos (cough), dolor de cabeza (headache), presion arterial (blood pressure), analisis de sangre (blood test), vacuna (vaccine), alergia (allergy), diagnostico (diagnosis), tratamiento (treatment), urgencias (emergency room), consulta (appointment), especialista (specialist), enfermero/a (nurse), farmacia (pharmacy), radiografia (X-ray), ecografia (ultrasound), quimioterapia (chemotherapy), rehabilitacion (rehabilitation), contagio (contagion), epidemia (epidemic), sistema inmunologico (immune system), donante (donor), trasplante (transplant), salud mental (mental health).

**Legal and Government (50 words):**
ley (law), derecho (right), juicio (trial), abogado/a (lawyer), juez (judge), demanda (lawsuit), prueba/evidencia (evidence), sentencia (sentence), culpable (guilty), inocente (innocent), testigo (witness), delito (crime), multa (fine), carcel/prision (jail/prison), libertad condicional (parole), constitucion (constitution), decreto (decree), ciudadano (citizen), votacion (vote), elecciones (elections), congreso (congress), senado (senate), diputado (representative), ministerio (ministry), gobernador (governor), alcalde (mayor), impuesto (tax), presupuesto (budget), deuda publica (public debt), reforma (reform).

**Food and Cooking (50 words):**
receta (recipe), ingrediente (ingredient), harina (flour), azucar (sugar), sal (salt), pimienta (pepper), aceite (oil), mantequilla (butter), ajo (garlic), cebolla (onion), tomate (tomato), lechuga (lettuce), zanahoria (carrot), papa/patata (potato), arroz (rice), frijoles/judias (beans), pollo (chicken), carne de res (beef), cerdo (pork), pescado (fish), mariscos (seafood), huevo (egg), queso (cheese), pan (bread), sopa (soup), ensalada (salad), postre (dessert), hornear (to bake), freir (to fry), hervir (to boil), asar (to roast/grill), picar (to chop), mezclar (to mix), sarten (frying pan), olla (pot), horno (oven), microondas (microwave), nevera/refrigerador (refrigerator), congelador (freezer), delicioso (delicious).

**Travel and Transportation (50 words):**
vuelo (flight), aeropuerto (airport), equipaje (luggage), maleta (suitcase), pasaporte (passport), visa (visa), aduana (customs), embarque (boarding), escala (layover), retraso (delay), billete/boleto (ticket), asiento (seat), ventanilla (window seat), pasillo (aisle seat), estacion (station), anden (platform), tren (train), autobus (bus), metro (subway), taxi (taxi), alquiler de coches (car rental), carretera (highway), peaje (toll), gasolina (gasoline), hotel (hotel), reserva (reservation), habitacion (room), recepcion (front desk), turismo (tourism), excursion (tour/trip), guia turistico (tour guide), monumento (monument), catedral (cathedral), museo (museum), playa (beach).

**Education (40 words):**
escuela (school), colegio (school/college), universidad (university), facultad (faculty/school), carrera (degree/major), asignatura/materia (subject), clase (class), aula (classroom), profesor/a (teacher/professor), alumno/estudiante (student), examen (exam), nota/calificacion (grade), aprobar (to pass), reprobar/suspender (to fail), tarea (homework), investigacion (research), tesis (thesis), beca (scholarship), matricula (enrollment/tuition), titulo (degree/diploma), licenciatura (bachelor's), maestria (master's), doctorado (doctorate), graduacion (graduation), biblioteca (library), laboratorio (laboratory), conferencia (lecture), seminario (seminar), apuntes (notes), cuaderno (notebook).

### 5.4 Idiomatic Expressions (50 Essential Idioms)

| Spanish | Literal Translation | Meaning |
|---------|-------------------|---------|
| Tomar el pelo | To take the hair | To joke/trick someone |
| Ser pan comido | To be eaten bread | To be very easy |
| Estar en las nubes | To be in the clouds | To be daydreaming |
| No tener pelos en la lengua | To not have hairs on the tongue | To speak bluntly |
| Meter la pata | To put in the paw | To put your foot in it |
| Costar un ojo de la cara | To cost an eye from the face | To be very expensive |
| Dar en el clavo | To hit the nail | To hit the nail on the head |
| Echar una mano | To throw a hand | To lend a hand |
| Ponerse las pilas | To put in one's batteries | To get one's act together |
| Tirar la toalla | To throw the towel | To give up |
| Estar como una cabra | To be like a goat | To be crazy |
| Ir al grano | To go to the grain | To get to the point |
| Quedarse en blanco | To stay in blank | To draw a blank |
| Ser una y carne | To be nail and flesh | To be inseparable |
| Llover sobre mojado | To rain on wet ground | To add insult to injury |
| Tener mala leche | To have bad milk | To be bad-tempered |
| Dar la lata | To give the can | To be annoying |
| Estar hasta las narices | To be up to the noses | To be fed up |
| No dar pie con bola | To not hit ball with foot | To not get anything right |
| Hacer la vista gorda | To make the fat view | To turn a blind eye |
| Tener mucha cara | To have a lot of face | To be shameless |
| Estar hecho polvo | To be made dust | To be exhausted |
| Dormir como un tronco | To sleep like a log | To sleep very deeply |
| No tener ni pies ni cabeza | To have neither feet nor head | To make no sense |
| Ser el colmo | To be the peak | To be the last straw |
| Echar lena al fuego | To throw wood on the fire | To add fuel to the fire |
| Estar entre la espada y la pared | To be between the sword and the wall | To be between a rock and a hard place |
| Matar dos pajaros de un tiro | To kill two birds with one shot | To kill two birds with one stone |
| Tener la sarten por el mango | To have the pan by the handle | To be in control |
| Buscarle tres pies al gato | To look for three feet on the cat | To overcomplicate things |

### 5.5 Regional Variations Deep Dive

**Voseo (Argentina, Uruguay, parts of Central America):**

| Tu conjugation | Vos conjugation | Example |
|---------------|-----------------|---------|
| tu hablas | vos hablas | Vos hablas ingles? |
| tu comes | vos comes | Que comes? |
| tu vives | vos vivis | Donde vivis? |
| tu tienes | vos tenes | Tenes tiempo? |
| tu eres | vos sos | Vos sos mi amigo. |
| tu puedes | vos podes | Podes venir? |
| tu quieres | vos queres | Que queres hacer? |

**Voseo in commands (affirmative):**
- Hablá (speak), comé (eat), viví (live), vení (come), decí (say).

**Mexican Spanish distinctive features:**
- Diminutive overuse: ahorita (right now), tantito (a tiny bit), cerquita (very close), rapidito (quickly).
- "Mande" instead of "Que?" when you didn't hear something.
- "Que onda?" (What's up?), "Orale" (Wow/Okay/Let's go), "Neta" (Really/Truth).
- "Padre" as an adjective meaning "cool": Que padre! (How cool!)
- "Chido" (cool), "Guey/Wey" (dude), "Naco" (tacky/low-class), "Fresa" (preppy/snobby).
- Heavy use of "pues": "Si, pues" (Yeah, well...), "Pues si" (Well, yes).

**Colombian Spanish distinctive features:**
- Extremely polite and formal, heavy use of "usted" even among friends and couples.
- "Pues" inserted frequently: "Si, pues" (Yeah, well...).
- "Bacano" (cool), "Parcero/Parce" (buddy), "Berraco" (tough/amazing), "Chimba" (cool/great).
- Clear pronunciation, considered one of the "cleanest" dialects.
- "Sumerce" (your grace) used in Boyaca region.
- "A la orden" (at your service) used constantly in shops.

**Spanish from Spain distinctive features:**
- Distinction between /s/ and /th/ (distincion): "caza" vs "casa" sound different.
- "Vosotros" for informal plural: Vosotros quereis ir? (Do you all want to go?)
- "Tio/Tia" (dude/girl), "Mola" (it's cool), "Flipar" (to be amazed), "Currar" (to work).
- "Vale" (okay) used constantly.
- "Coger" means "to take/grab" (in LatAm it has a vulgar meaning).
- Leismo: using "le" instead of "lo" for masculine direct objects.

**Chilean Spanish distinctive features:**
- Aspiration of final -s: "Estamos" sounds like "Ehtamoh".
- "Cachai?" (Do you get it?), "Po" (pues), "Fome" (boring), "Bacán" (cool).
- Heavy use of "-ai" ending: "Tu estai bien?" instead of "Tu estas bien?"

**Caribbean Spanish (Cuba, DR, Puerto Rico):**
- Aspiration or deletion of -s: "Estas" becomes "Ehtah" or "Etah".
- Deletion of final -d: "Ciudad" becomes "Ciuda".
- "Asere" (buddy - Cuba), "Que lo que" (What's up - DR).

### 5.6 Discourse Connectors and Transition Words

**Adding information:** ademas (moreover), tambien (also), asimismo (likewise), igualmente (equally), incluso (even), es mas (furthermore).

**Contrasting:** sin embargo (however), no obstante (nevertheless), aunque (although), a pesar de (despite), por el contrario (on the contrary), en cambio (on the other hand).

**Cause and effect:** porque (because), ya que (since), puesto que (given that), por lo tanto (therefore), por consiguiente (consequently), de modo que (so that), asi que (so).

**Sequencing:** en primer lugar (firstly), en segundo lugar (secondly), a continuacion (next), luego (then), finalmente (finally), por ultimo (lastly).

**Summarizing:** en resumen (in summary), en conclusion (in conclusion), en definitiva (ultimately), para resumir (to summarize), en pocas palabras (in a few words).

---

## Part 6: Comprehensive Exercises

### Exercise Set A: Fill in the Blank (Present Tense)
1. Yo _____ (hablar) espanol todos los dias.
2. Ella _____ (comer) en el restaurante.
3. Nosotros _____ (vivir) en una casa grande.
4. Tu _____ (querer) ir al cine?
5. Ellos no _____ (poder) venir hoy.
6. Yo _____ (conocer) a tu hermana.
7. Usted _____ (tener) razon.
8. Nosotros _____ (ir) al parque los domingos.

**Answers:** 1-hablo, 2-come, 3-vivimos, 4-quieres, 5-pueden, 6-conozco, 7-tiene, 8-vamos.

### Exercise Set B: Preterite vs. Imperfect
1. Ayer yo _____ (ir) al supermercado.
2. Cuando yo _____ (ser) nino, _____ (jugar) en el parque.
3. Ella _____ (leer) un libro cuando yo _____ (llegar).
4. Nosotros _____ (comer) pizza todos los viernes. (habitual)
5. El ano pasado, ellos _____ (viajar) a Espana.
6. _____ (Ser) las tres de la tarde cuando _____ (empezar) a llover.
7. Mi abuela siempre me _____ (contar) cuentos.
8. De repente, el telefono _____ (sonar).

**Answers:** 1-fui, 2-era/jugaba, 3-leia/llegue, 4-comiamos, 5-viajaron, 6-Eran/empezo, 7-contaba, 8-sono.

### Exercise Set C: Subjunctive
1. Quiero que tu _____ (venir) a mi fiesta.
2. Es importante que nosotros _____ (estudiar).
3. Dudo que el _____ (saber) la respuesta.
4. Ojala que _____ (hacer) buen tiempo manana.
5. Busco un apartamento que _____ (tener) balcon.
6. Me alegra que ustedes _____ (estar) aqui.
7. No creo que ella _____ (poder) venir.
8. Es necesario que tu _____ (ir) al medico.

**Answers:** 1-vengas, 2-estudiemos, 3-sepa, 4-haga, 5-tenga, 6-esten, 7-pueda, 8-vayas.

### Exercise Set D: Translate to Spanish
1. I would travel to Spain if I had more money.
2. She told me that she would call me tomorrow.
3. We have lived here for five years.
4. I hope you feel better soon.
5. The book that I read was very interesting.
6. If I had studied more, I would have passed the exam.
7. They want us to arrive early.
8. It is said that this restaurant is the best in the city.

**Answers:**
1. Viajaria a Espana si tuviera mas dinero.
2. Me dijo que me llamaria manana.
3. Hemos vivido aqui por cinco anos.
4. Espero que te sientas mejor pronto.
5. El libro que lei fue muy interesante.
6. Si hubiera estudiado mas, habria aprobado el examen.
7. Quieren que lleguemos temprano.
8. Se dice que este restaurante es el mejor de la ciudad.

### Exercise Set E: Por vs. Para
1. Gracias _____ tu ayuda.
2. Este regalo es _____ mi madre.
3. Caminamos _____ el parque.
4. Estudio _____ aprobar el examen.
5. Pague veinte dolares _____ el libro.
6. La tarea es _____ manana.
7. Trabajo _____ una empresa internacional.
8. Hablamos _____ telefono.

**Answers:** 1-por, 2-para, 3-por, 4-para, 5-por, 6-para, 7-para, 8-por.

### Exercise Set F: Commands
1. (Tu, affirmative) _____ (hablar) mas despacio.
2. (Tu, negative) No _____ (comer) eso.
3. (Usted, affirmative) _____ (venir) aqui, por favor.
4. (Tu, affirmative) _____ (decir) la verdad.
5. (Tu, negative) No _____ (salir) de noche.
6. (Ustedes, affirmative) _____ (sentarse), por favor.

**Answers:** 1-Habla, 2-comas, 3-Venga, 4-Di, 5-salgas, 6-Sientense.

---

## Part 7: Conversation Templates

### 7.1 At a Restaurant
- Mesero: Buenas noches. Mesa para cuantos?
- Cliente: Para dos, por favor.
- Mesero: Aqui tienen el menu. Desean algo de beber?
- Cliente: Yo quiero una copa de vino tinto y ella quiere agua con gas.
- Mesero: Ya saben que van a pedir?
- Cliente: Si, yo voy a pedir el filete con papas fritas y ella va a pedir la ensalada Cesar.
- Mesero: Perfecto. Algo mas?
- Cliente: No, gracias. Ah, y la cuenta cuando pueda, por favor.
- Mesero: Aqui tiene la cuenta. Son cuarenta y cinco euros.
- Cliente: Puedo pagar con tarjeta?
- Mesero: Si, claro. Aqui tiene el datafono.

### 7.2 At the Doctor
- Doctor: Buenos dias. Que le pasa?
- Paciente: Me duele mucho la garganta y tengo fiebre desde hace dos dias.
- Doctor: Tiene otros sintomas? Tos, dolor de cabeza?
- Paciente: Si, tambien tengo tos seca y me duele el cuerpo.
- Doctor: Voy a examinarlo. Abra la boca, por favor... Tiene una infeccion. Le voy a recetar un antibiotico.
- Paciente: Cuantas veces al dia debo tomarlo?
- Doctor: Dos veces al dia, despues de comer, durante siete dias. Si no mejora en tres dias, vuelva a la consulta.
- Paciente: Puedo ir a trabajar?
- Doctor: Le recomiendo que descanse al menos dos dias.

### 7.3 Job Interview
- Entrevistador: Cuenteme sobre usted.
- Candidato: Soy ingeniero de software con cinco anos de experiencia. Actualmente trabajo en una empresa de tecnologia donde lidero un equipo de desarrollo.
- Entrevistador: Por que quiere cambiar de trabajo?
- Candidato: Busco nuevos desafios y oportunidades de crecimiento profesional. Me interesa mucho la mision de esta empresa.
- Entrevistador: Cuales son sus fortalezas?
- Candidato: Soy muy organizado, trabajo bien en equipo y me adapto rapidamente a nuevas tecnologias.
- Entrevistador: Y sus debilidades?
- Candidato: A veces soy demasiado perfeccionista, pero he aprendido a priorizar y delegar.
- Entrevistador: Donde se ve en cinco anos?
- Candidato: Me gustaria estar liderando proyectos innovadores y contribuyendo al crecimiento de la empresa.

### 7.4 At the Airport
- Agente: Buenos dias. Su pasaporte y boleto, por favor.
- Viajero: Aqui tiene.
- Agente: Va a documentar equipaje?
- Viajero: Si, una maleta.
- Agente: Pongala en la bascula, por favor... Son 22 kilos, esta bien. Prefiere ventanilla o pasillo?
- Viajero: Ventanilla, por favor.
- Agente: Aqui tiene su pase de abordar. Puerta B7, el embarque comienza a las 14:30.
- Viajero: A que hora sale el vuelo?
- Agente: A las 15:00. Buen viaje!

### 7.5 Shopping for Clothes
- Vendedor: Buenas tardes. En que puedo ayudarle?
- Cliente: Estoy buscando una camisa para una entrevista de trabajo.
- Vendedor: Que talla usa?
- Cliente: Mediana, creo. Puedo probarme esta azul?
- Vendedor: Claro, los probadores estan al fondo a la derecha.
- Cliente: Me queda un poco grande. Tiene una talla mas pequena?
- Vendedor: Si, aqui tiene. Esta le quedara mejor.
- Cliente: Perfecta. Cuanto cuesta?
- Vendedor: Cuarenta y cinco dolares. Hoy tenemos un 20% de descuento.
- Cliente: Genial, me la llevo. Puedo pagar con tarjeta?

### 7.6 Renting an Apartment
- Inquilino: Hola, llamo por el anuncio del apartamento en alquiler.
- Dueno: Si, todavia esta disponible. Es un apartamento de dos habitaciones con un bano.
- Inquilino: Cuanto es el alquiler mensual?
- Dueno: Ochocientos euros al mes, mas los servicios.
- Inquilino: Los servicios estan incluidos?
- Dueno: No, el agua, la luz y el internet se pagan aparte. Son aproximadamente cien euros mas.
- Inquilino: Se permite tener mascotas?
- Dueno: Si, perros pequenos y gatos estan permitidos.
- Inquilino: Puedo ir a verlo manana?
- Dueno: Si, le parece bien a las diez de la manana?

---

## Part 8: Writing and Formal Communication

### 8.1 Formal Letter Structure
```
[Ciudad], [dia] de [mes] de [ano]

Estimado/a Sr./Sra. [Apellido]:

Me dirijo a usted con el fin de [proposito].

[Cuerpo de la carta - parrafos con informacion detallada]

Agradezco de antemano su atencion.

Atentamente / Cordialmente,
[Nombre completo]
[Cargo/Titulo]
[Informacion de contacto]
```

### 8.2 Email Conventions
- Formal opening: Estimado/a [nombre], / Distinguido/a [nombre],
- Semi-formal: Hola [nombre], / Buenos dias [nombre],
- Formal closing: Atentamente, / Cordialmente, / Quedo a su disposicion.
- Semi-formal closing: Un saludo, / Saludos cordiales,

### 8.3 Common Written Expressions
- En relacion con / Con respecto a (Regarding)
- Le informo que (I inform you that)
- Adjunto encontrara (Attached you will find)
- Quedo a la espera de su respuesta (I await your response)
- No dude en contactarme (Don't hesitate to contact me)
- Lamento informarle que (I regret to inform you that)
- Me complace comunicarle que (I am pleased to inform you that)

---

## References and Resources

- Real Academia Espanola (RAE) - rae.es
- Instituto Cervantes - cervantes.es
- Common European Framework of Reference for Languages (CEFR) - Council of Europe
- SpanishDict - spanishdict.com
- WordReference - wordreference.com
- Fundeu (Fundacion del Espanol Urgente) - fundeu.es
- Diccionario Panhispanico de Dudas - Real Academia Espanola


---

## Part 9: Additional Grammar Topics

### 9.1 Comparatives and Superlatives

**Comparisons of inequality:**
- mas + adjective/adverb + que: El es mas alto que yo. (He is taller than me.)
- menos + adjective/adverb + que: Ella es menos timida que su hermana. (She is less shy than her sister.)
- mas/menos + noun + que: Tengo mas libros que tu. (I have more books than you.)
- verb + mas/menos + que: Ella estudia mas que yo. (She studies more than me.)

**Comparisons of equality:**
- tan + adjective/adverb + como: El es tan inteligente como ella. (He is as intelligent as her.)
- tanto/a/os/as + noun + como: Tengo tantos libros como tu. (I have as many books as you.)
- verb + tanto como: Ella trabaja tanto como yo. (She works as much as me.)

**Irregular comparatives:**
- bueno to mejor (better), malo to peor (worse)
- grande to mayor (older/greater), pequeno to menor (younger/lesser)
- mucho to mas (more), poco to menos (less)

**Superlatives:**
- el/la/los/las + mas/menos + adjective + de: Es la mas inteligente de la clase. (She is the smartest in the class.)
- Absolute superlative (-isimo/a): Es altisimo. (He is extremely tall.) / Es facilisimo. (It's extremely easy.)

### 9.2 The Gerund and Infinitive as Complements

**Verbs followed by infinitive (no preposition):**
querer, poder, deber, necesitar, saber, preferir, desear, esperar, lograr, soler, pensar (plan to).

**Verbs followed by "a" + infinitive:**
ir a, empezar a, comenzar a, aprender a, ayudar a, ensenar a, invitar a, volver a, atreverse a, dedicarse a.

**Verbs followed by "de" + infinitive:**
dejar de, tratar de, terminar de, acabar de, acordarse de, olvidarse de, tener ganas de.

**Verbs followed by "en" + infinitive:**
insistir en, pensar en, tardar en, consistir en, quedar en.

**Verbs followed by "con" + infinitive:**
sonar con, contar con, amenazar con.

### 9.3 Diminutives and Augmentatives

**Diminutives (express smallness, affection, or informality):**
- -ito/a (most common): perro to perrito, casa to casita, momento to momentito.
- -cito/a (after words ending in -e, -n, -r): cafe to cafecito, joven to jovencito, amor to amorcito.
- -illo/a (regional, sometimes pejorative): guerra to guerrilla, palo to palillo.
- -ico/a (Colombia, Costa Rica): momento to momentico, gato to gatico.

**Augmentatives (express largeness, intensity, or sometimes negativity):**
- -on/ona: casa to casona, hombre to hombron, soltera to solterona.
- -ote/ota: grande to grandote, amigo to amigote.
- -azo/aza: perro to perrazo, coche to cochazo (also means "great/impressive").

### 9.4 Prepositions in Depth

**A (to, at, personal "a"):**
- Direction: Voy a la tienda. (I'm going to the store.)
- Time: Llego a las tres. (I arrive at three.)
- Personal "a" (before human direct objects): Veo a mi madre. (I see my mother.)
- After verbs of motion: Vengo a ayudarte. (I come to help you.)

**De (of, from, about):**
- Origin: Soy de Mexico. (I'm from Mexico.)
- Possession: El libro de Maria. (Maria's book.)
- Material: Una mesa de madera. (A wooden table.)
- Topic: Hablamos de politica. (We talked about politics.)

**En (in, on, at):**
- Location: Estoy en casa. (I'm at home.)
- Time period: En enero. (In January.) / En dos horas. (In two hours.)
- Means: Voy en coche. (I go by car.)
- Surface: El libro esta en la mesa. (The book is on the table.)

**Con (with):**
- Accompaniment: Voy con mi amigo. (I go with my friend.)
- Instrument: Escribo con un lapiz. (I write with a pencil.)
- Conmigo, contigo, consigo (with me, with you, with himself/herself).

**Sin (without):**
- Sin azucar. (Without sugar.)
- Sin embargo. (However/Nevertheless.)

**Sobre (on, about, over):**
- El libro esta sobre la mesa. (The book is on the table.)
- Un documental sobre la guerra. (A documentary about the war.)

**Hacia (toward):**
- Caminamos hacia el norte. (We walked toward the north.)

**Hasta (until, up to):**
- Trabajo hasta las cinco. (I work until five.)
- Camina hasta la esquina. (Walk up to the corner.)

**Desde (from, since):**
- Vivo aqui desde 2010. (I've lived here since 2010.)
- Desde mi casa hasta la oficina. (From my house to the office.)

### 9.5 Subjunctive in Adverbial Clauses

**Always subjunctive (ESCAPA):**
- En caso de que (in case): Lleva paraguas en caso de que llueva.
- Sin que (without): Salio sin que nadie lo viera.
- Con tal de que (provided that): Ire con tal de que tu vayas.
- Antes de que (before): Llamame antes de que salgas.
- Para que (so that): Te lo explico para que entiendas.
- A menos que (unless): No ire a menos que me invites.

**Subjunctive or indicative (depends on experience):**
- Cuando (when): Cuando llegues, llamame. (future/subjunctive) vs. Cuando llego, siempre como. (habitual/indicative)
- Hasta que (until): Espera hasta que yo vuelva. (future) vs. Siempre espero hasta que el llega. (habitual)
- Despues de que (after): Despues de que termines, descansa. (future) vs. Despues de que termino, descanso. (habitual)
- Aunque (although/even if): Aunque llueva, ire. (uncertain) vs. Aunque llueve, voy. (known fact)

---

## Part 10: Cultural Competence

### 10.1 Formal vs. Informal Register

Spanish has a deeply ingrained system of formality that affects pronoun choice, verb conjugation, and overall communication style.

**When to use "tu" (informal):**
- Friends and peers of similar age
- Family members
- Children
- Colleagues in casual workplaces
- Social media and informal writing

**When to use "usted" (formal):**
- Strangers, especially older people
- Professional settings (boss, clients)
- Customer service interactions
- Academic settings (professor to student may vary)
- Official documents and formal correspondence
- First meetings (until invited to use "tu")

**Transitioning from usted to tu:**
- "Puedes tutearme" (You can use tu with me)
- "Tratame de tu" (Address me informally)

### 10.2 Cultural Norms in Spanish-Speaking Countries

**Greetings and physical contact:**
- One kiss on the cheek (most of Latin America) or two kisses (Spain) when greeting friends.
- Handshake for formal/business introductions.
- Hugs (abrazos) are common among close friends and family.

**Time and punctuality:**
- "Hora latina" - social events often start 30-60 minutes after the stated time.
- Business meetings are generally more punctual.
- "Ahorita" in Mexico can mean "right now" or "in a while" depending on context.

**Dining customs:**
- Lunch (almuerzo/comida) is typically the largest meal, eaten between 1-3 PM.
- Dinner (cena) is lighter and later (8-10 PM in Spain, 7-9 PM in Latin America).
- "Sobremesa" - the tradition of lingering at the table after a meal for conversation.
- It's polite to keep hands visible on the table (not on your lap).

**Business etiquette:**
- Titles matter: Licenciado/a, Ingeniero/a, Doctor/a are used professionally.
- Business cards are exchanged formally.
- Relationship-building often precedes business discussions.
- "Manana" in business context doesn't always mean literally tomorrow.

### 10.3 False Cognates (False Friends)

| Spanish Word | Looks Like | Actually Means | English Word Is |
|-------------|-----------|---------------|----------------|
| Actual | Actual | Current/present | Real/verdadero |
| Asistir | Assist | To attend | Ayudar |
| Carpeta | Carpet | Folder | Alfombra |
| Constipado | Constipated | Having a cold | Estrenido |
| Embarazada | Embarrassed | Pregnant | Avergonzada |
| Exito | Exit | Success | Salida |
| Libreria | Library | Bookstore | Biblioteca |
| Realizar | Realize | To carry out/accomplish | Darse cuenta |
| Sensible | Sensible | Sensitive | Sensato |
| Soportar | Support | To tolerate/bear | Apoyar |
| Recordar | Record | To remember | Grabar |
| Largo | Large | Long | Grande |
| Molestar | Molest | To bother/annoy | Abusar |
| Pretender | Pretend | To try/attempt | Fingir |
| Contestar | Contest | To answer | Competir |

### 10.4 Proverbs and Sayings (Refranes)

- Mas vale tarde que nunca. (Better late than never.)
- No hay mal que por bien no venga. (Every cloud has a silver lining.)
- Dime con quien andas y te dire quien eres. (Tell me who you walk with and I'll tell you who you are.)
- A caballo regalado no se le mira el diente. (Don't look a gift horse in the mouth.)
- El que mucho abarca, poco aprieta. (He who grasps at too much holds nothing firmly.)
- Mas vale prevenir que curar. (Prevention is better than cure.)
- En boca cerrada no entran moscas. (Flies don't enter a closed mouth. = Silence is golden.)
- Cada maestrillo tiene su librillo. (Every teacher has their own little book. = Everyone has their own way.)
- No hay rosa sin espinas. (There is no rose without thorns.)
- Quien mucho duerme, poco aprende. (He who sleeps a lot, learns little.)
- A mal tiempo, buena cara. (In bad weather, put on a good face. = Keep a stiff upper lip.)
- Ojos que no ven, corazon que no siente. (Eyes that don't see, heart that doesn't feel. = Out of sight, out of mind.)
- Del dicho al hecho hay mucho trecho. (From saying to doing there's a long stretch. = Easier said than done.)
- Mas sabe el diablo por viejo que por diablo. (The devil knows more from being old than from being the devil. = Experience is the best teacher.)
- Perro que ladra no muerde. (A barking dog doesn't bite.)

---

## Appendix: Quick Reference Conjugation Summary

### All Tenses of "Hablar" (Regular -AR Model)

| Tense | Yo | Tu | El | Nosotros | Ellos |
|-------|----|----|-----|----------|-------|
| Present Indicative | hablo | hablas | habla | hablamos | hablan |
| Preterite | hable | hablaste | hablo | hablamos | hablaron |
| Imperfect | hablaba | hablabas | hablaba | hablabamos | hablaban |
| Future | hablare | hablaras | hablara | hablaremos | hablaran |
| Conditional | hablaria | hablarias | hablaria | hablariamos | hablarian |
| Present Subjunctive | hable | hables | hable | hablemos | hablen |
| Imperfect Subjunctive | hablara | hablaras | hablara | hablaramos | hablaran |
| Present Perfect | he hablado | has hablado | ha hablado | hemos hablado | han hablado |
| Pluperfect | habia hablado | habias hablado | habia hablado | habiamos hablado | habian hablado |
| Future Perfect | habre hablado | habras hablado | habra hablado | habremos hablado | habran hablado |
| Conditional Perfect | habria hablado | habrias hablado | habria hablado | habriamos hablado | habrian hablado |

### All Tenses of "Tener" (Common Irregular)

| Tense | Yo | Tu | El | Nosotros | Ellos |
|-------|----|----|-----|----------|-------|
| Present Indicative | tengo | tienes | tiene | tenemos | tienen |
| Preterite | tuve | tuviste | tuvo | tuvimos | tuvieron |
| Imperfect | tenia | tenias | tenia | teniamos | tenian |
| Future | tendre | tendras | tendra | tendremos | tendran |
| Conditional | tendria | tendrias | tendria | tendriamos | tendrian |
| Present Subjunctive | tenga | tengas | tenga | tengamos | tengan |
| Imperfect Subjunctive | tuviera | tuvieras | tuviera | tuvieramos | tuvieran |
| Present Perfect | he tenido | has tenido | ha tenido | hemos tenido | han tenido |

### All Tenses of "Ir" (Highly Irregular)

| Tense | Yo | Tu | El | Nosotros | Ellos |
|-------|----|----|-----|----------|-------|
| Present Indicative | voy | vas | va | vamos | van |
| Preterite | fui | fuiste | fue | fuimos | fueron |
| Imperfect | iba | ibas | iba | ibamos | iban |
| Future | ire | iras | ira | iremos | iran |
| Conditional | iria | irias | iria | iriamos | irian |
| Present Subjunctive | vaya | vayas | vaya | vayamos | vayan |
| Imperfect Subjunctive | fuera | fueras | fuera | fueramos | fueran |
| Present Perfect | he ido | has ido | ha ido | hemos ido | han ido |

---

*End of Spanish Teacher Supreme Master Guide. Total coverage: A1 through C2, all major tenses, comprehensive vocabulary, regional variations, cultural competence, and practical conversation templates.*

## === FILE: 35-spanish-teacher-troubleshooting.md ===
# 35 - Spanish Teacher (Troubleshooting Common Learner Errors)

## 1. Ser vs. Estar Confusion
**Error:** "Soy aburrido" (I am a boring person) instead of "Estoy aburrido" (I am bored).
**Diagnosis:** Learner is translating the English "I am" directly without considering the permanence vs. temporary state rule.
**Fix:** Apply the DOCTOR (Description, Occupation, Characteristic, Time, Origin, Relationship) acronym for Ser, and PLACE (Position, Location, Action, Condition, Emotion) for Estar.

## 2. Por vs. Para Mix-ups
**Error:** "Trabajo para tres horas" instead of "Trabajo por tres horas".
**Diagnosis:** Learner equates both to "for" without understanding the underlying concept of duration vs. destination.
**Fix:** Use "por" when looking back at the cause or looking at the duration. Use "para" when looking forward to the destination or goal.

## 3. Preterite vs. Imperfect Selection
**Error:** "Ayer, el sol brilló y el cielo fue azul." (Yesterday, the sun shone and the sky was blue - using preterite for description).
**Diagnosis:** Learner is using preterite for all past actions, ignoring the descriptive nature of the imperfect.
**Fix:** "Ayer, el sol brillaba y el cielo era azul." Use imperfect for setting the scene, weather, age, and ongoing past states.

## 4. Gender Disagreement
**Error:** "El mano" or "La problema".
**Diagnosis:** Learner assumes all words ending in 'o' are masculine and 'a' are feminine.
**Fix:** Memorize the exceptions. "La mano" (hand), "La radio" (radio), "La foto" (photo). Words ending in -ma are often of Greek origin and are masculine: "El problema", "El sistema", "El clima".

## 5. Subject Pronoun Overuse
**Error:** "Yo voy a la tienda y yo compro manzanas."
**Diagnosis:** Direct translation from English, where subject pronouns are mandatory.
**Fix:** Drop the pronouns. The verb conjugation already indicates the subject. "Voy a la tienda y compro manzanas."

