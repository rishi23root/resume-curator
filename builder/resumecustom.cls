% Intro Options
\ProvidesClass{resumecustom}[2014/04/30 CV class]
\NeedsTeXFormat{LaTeX2e}
\DeclareOption{print}{\def\@cv@print{}}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}
}
\ProcessOptions\relax
\LoadClass{article}

% Package Imports
\usepackage[hmargin=1.25cm, vmargin=0.75cm]{geometry}
\usepackage[hidelinks]{hyperref}

% Publications
\usepackage{cite}
\renewcommand\refname{\vskip -1.5cm}

% Color definitions
\usepackage[usenames,dvipsnames]{xcolor} 
\definecolor{date}{HTML}{666666} 
\definecolor{primary}{HTML}{2b2b2b} 
\definecolor{headings}{HTML}{6A6A6A}
\definecolor{subheadings}{HTML}{333333}

% Set main fonts
\usepackage{lmodern} % Use lmodern font package instead of fontspec

% Date command
\usepackage[absolute]{textpos}
\usepackage[UKenglish]{isodate}
\setlength{\TPHorizModule}{1mm}
\setlength{\TPVertModule}{1mm}
\newcommand{\lastupdated}{\begin{textblock}{60}(155,5)
\color{date}\fontfamily{lmr}\fontsize{8pt}{10pt}\selectfont 
Last Updated on \today
\end{textblock}}

% Name command
\newcommand{\namesection}[3]{
\centering{
\fontsize{30pt}{45pt}\selectfont 
\fontfamily{lmr}\selectfont #1 
\fontfamily{lmr}\selectfont #2
} \\[5pt]
\centering{
\color{headings}
\fontfamily{lmr}\fontsize{11pt}{14pt}\selectfont #3}
\noindent\makebox[\linewidth]{\color{headings}\rule{\paperwidth}{0.4pt}}
\vspace{-15pt}
}
\newcommand{\namesectionsinglelayout}[3]{
\centering{
  \fontsize{30pt}{45pt}\selectfont 
  \fontfamily{lmr}\selectfont #1 
  \fontfamily{lmr}\selectfont #2
} \\[5pt]
\centering{
  \color{headings}
  \fontfamily{lmr}\fontsize{11pt}{-14pt}\selectfont #3
  \vspace{-10pt}
}
\vspace{5pt}
}

% Section separators 
\usepackage{titlesec}
\titlespacing{\section}{0pt}{0pt}{0pt} 
\titlespacing{\subsection}{0pt}{0pt}{0pt}
\newcommand{\sectionsep}{\vspace{8pt}}

% Headings command
\titleformat{\section}{\color{headings}
\scshape\fontfamily{lmr}\fontsize{16pt}{24pt}\selectfont \raggedright\uppercase}{}{0em}{}

% Subheadings command
\titleformat{\subsection}{
\color{subheadings}\fontfamily{lmr}\fontsize{12pt}{12pt}\selectfont\bfseries\uppercase}{}{0em}{}

\newcommand{\runsubsection}[1]{
\color{subheadings}\fontfamily{lmr}\fontsize{12pt}{12pt}\selectfont\bfseries\uppercase {#1} \normalfont}

% Descriptors command
\newcommand{\descript}[1]{
\color{subheadings}\raggedright\scshape\fontfamily{lmr}\fontsize{11pt}{13pt}\selectfont {#1 \\} \normalfont}

% Location command
\newcommand{\location}[1]{
\color{headings}\raggedright\fontfamily{lmr}\fontsize{10pt}{12pt}\selectfont {#1\\} \normalfont}

% Bullet Lists with fewer gaps command
\newenvironment{tightemize}{
\vspace{-\topsep}\begin{itemize}\itemsep1pt \parskip0pt \parsep0pt}
{\end{itemize}\vspace{-\topsep}}



% field command for single page layouts 
\newcommand{\fieldsection}[2]{%
  \vspace{-10pt}
  \section*{\small \textbf{#1}}
  \vspace{-2pt}
  \hrule % Add horizontal line under section name
  \vspace{1em}
  \hspace*{1.5em}
  \begin{minipage}{0.95\linewidth} % Set section width to 90% of the page width
    #2 % Content of the section
  \end{minipage}
  \vspace{0.5em}
}