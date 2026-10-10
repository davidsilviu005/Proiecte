# RGD Horror Story

**Un proiect horror 3D realizat în Unity de o echipă de cinci membri.** Explorează, caută indicii și resurse, gestionează lumina lanternei și păstrează-ți luciditatea într-un mediu construit pentru suspans.

> [!NOTE]
> Proiectul este în dezvoltare. Scena `SampleScene` configurată în Build Settings este momentan o scenă de bază; sistemele de joc se află în cod și în asseturile proiectului, dar depozitul nu include încă un nivel final gata de jucat.

## Despre proiect

RGD Horror Story combină explorarea la persoana întâi cu mecanici de supraviețuire și investigație. Jucătorul poate interacționa cu obiecte din apropiere, aduna indicii, baterii, pastile și chei, apoi folosi resursele pentru a progresa. Întunericul afectează nivelul de luciditate, iar lanterna are o baterie limitată.

### Sisteme implementate

- **Explorare și interacțiune:** interacțiune cu obiecte și uși prin raycast.
- **Inventar:** evidența bateriilor, pastilelor și cheilor colectate.
- **Lanternă și luciditate:** consumul bateriei, reîncărcare și efecte vizuale asociate scăderii nivelului de luciditate.
- **Indicii:** colectare și afișare într-un meniu dedicat.
- **Uși și chei:** uși care pot necesita o anumită cheie.
- **Salvare și încărcare:** poziția jucătorului, resursele, indiciile, cheile și progresul unor evenimente audio sunt stocate local în JSON.
- **Interfață:** meniuri de start, pauză, salvare/încărcare și setări audio.

## Tehnologii

- **Unity:** `6000.3.19f1`
- **Limbaj:** C#
- **Randare:** Universal Render Pipeline (URP)
- **Pachete relevante:** Input System, AI Navigation, TextMesh Pro și Unity UI

## Cum deschizi proiectul

1. Clonează depozitul folosind adresa afișată de butonul **Code** de pe GitHub sau descarcă arhiva ZIP.
2. Deschide **Unity Hub** și alege **Add project from disk**.
3. Selectează folderul clonat și deschide-l cu **Unity 6000.3.19f1**.
4. Așteaptă importul asseturilor și al pachetelor. Scena inclusă în Build Settings este `Assets/Scenes/SampleScene.unity`.

> Pentru a obține un nivel jucabil, mecanicile din `Assets/Scripts/` trebuie configurate într-o scenă de joc. Scena inclusă momentan nu reprezintă o versiune finală.

## Comenzi prevăzute de scripturi

| Acțiune | Tastă |
| --- | --- |
| Deplasare | `W` `A` `S` `D` |
| Privire în jur | Mouse |
| Interacțiune | `E` |
| Lanternă pornit/oprit | `F` |
| Schimbă bateria lanternei | `R` |
| Folosește o pastilă | `Q` |
| Vezi inventarul | `Tab` |
| Deschide lista de indicii | `C` |
| Meniu de pauză | `M` |
| Meniu salvare/încărcare | `Esc` |

Disponibilitatea comenzilor depinde de configurarea scenei și a componentelor corespunzătoare.

## Structura proiectului

```text
Assets/
├── Scenes/              # Scenele Unity
├── Scripts/             # Sistemele de joc și interfața
├── UI/                  # Elemente pentru interfață
├── TexturesRGD/         # Texturi folosite de proiect
└── ...                  # Alte asseturi și pachete importate
Packages/                # Dependențele Unity
ProjectSettings/          # Configurația proiectului
```

## Echipa

- David Silviu
- Argatu Ioan-Dinu
- Dumitrescu Vlad-Ionu
- Nicolae Theodor
- Ghiduc Alexandru

## Asseturi externe

Depozitul conține și asseturi importate de la terți. Drepturile asupra acestora aparțin autorilor lor; verifică documentația și licențele fiecărui pachet înainte de redistribuire.
