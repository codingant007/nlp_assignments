#Sentence segmentation heuristics

- Consider the following as sentence boundaries
	- `!`
	- `?`
	- `.`

- Move the boundary if `"` exist
	- She turned to him, "This is great." she said.
	=> ["She turned to him, \"This is great.\" she said."]
	- In case double quotes is followed by lowecase letter merge the following sentence.

- Disqualify `.` if 
	- Preceeded by a valid abbrevation

- Disqualify `!` or `?` if
	- Followed by lowercase.


#Abbrevation heuristics
- One letter uppercase
	- ['U.S.', 'A. Nikhil']
- Two letter Upper
	- ['Mt. Everest', 'Mr. Langdon', 'Pitt Briggs & Co.', 'St. Louise Church', 'Frank Jr. is a funny man.']
- One or Two letter words followed by non-capital alphabet
	- ['Jane and co. came to the party', 'turn to p. 35']


#Word segmentation heuristics

- Word can be preceeded by
	- ^
	- Space
	- Punctuation
		- `"`
		- `'`
- Word can be follwed by
	- Punctuation
		- `,`
		- `.`
		- `;`
		- `'`
		- `"`
	- Annotation
		- `?`
		- `!`

- Nikhil's must be a single word
- At-least must be a single word
- Phones' must be a single word
- 100.00 must be a single word
- Mr. Alamanda must be a single word

- $ handling
- 