\version "2.22.1"
\header {

tagline = ##f}


headSquare = {\once \override NoteHead.stencil = #ly:text-interface::print
\once \override NoteHead.text = #(markup #:musicglyph "noteheads.s2laWalker" )
}
headSlash = {\once \override NoteHead.stencil = #ly:text-interface::print
\once \override NoteHead.text = #(markup #:musicglyph "noteheads.s0slash" )
}
glissOn = {\override NoteColumn.glissando-skip =  ##t
    \hide NoteHead
    \omit Accidental
    \override NoteHead.no-ledgers =  ##t
}
glissOff = {\revert NoteColumn.glissando-skip
    \undo \hide NoteHead
    \undo \omit Accidental
    \revert NoteHead.no-ledgers
}
\score {
<<\new Staff \with {
\omit TimeSignature
}
{
\time 8/4
gis'16\ff ( b'16\< gis'16 a'16 b'16 cis''16 f''16 dis''16 f''16 fis''16 f''16 fis''16) gis''4\fff\glissando\glissOn  \hide NoteHead  \once\omit Accidental \glissOff fis''4 \undo \hide NoteHead r2\! r4
}>>}
