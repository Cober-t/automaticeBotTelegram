from mdutils import MdUtils
from definitions import Obsidian


class MarkDownFileUtils:
	'''Utils for manage files from Obsidian'''

	mdFile = None

	@staticmethod
	def createFile(path, name):
		mdFile = MdUtils(file_name=path, title='Markdown file Example')



VAULT_DIRECTORY = "Z:\\Jorge Tejado\\ObsidianVault\\"
FILE = "Z:\\Jorge Tejado\\ObsidianVault\\Apuntes\\ejemplo.md"

### Retrieve File
mdFile = MdUtils(file_name=FILE, title='Markdown file Example')


## Create headers
# mdFile.new_header(level=1, title='Header', header_id='firstheader')
# mdFile.new_header(level=1, title='Setext Header 1', style='setext')
# mdFile.new_header(level=2, title='Setext Header 2', style='setext')


# Create Paragraph
mdFile.new_header(level=1, title='PARAGAPH EXAMPLE', header_id='paragraph')
mdFile.new_paragraph("Paragraph created, bold and italics text.", bold_italics_code='bi', color='purple')
mdFile.write('  \n')

# Create Line
mdFile.new_header(level=1, title='NEW LINE EXAMPLE', header_id='line')
mdFile.new_line("Line created``new_line`` method.\n")
# Create list


# Write method
mdFile.new_header(level=1, title='WRITE EXAMPLE', header_id='write')
mdFile.write('  \n')
mdFile.write("The following text has been written with ``write`` method. You can use markdown directives to write:"
			 "**bold**, _italics_, ``inline_code``... or ")
mdFile.write("use the following available parameters:  \n")
mdFile.write('  \n')
mdFile.write('bold_italics_code', bold_italics_code='bic')
mdFile.write('  \n')
mdFile.write('Text color\n', color='green')
mdFile.write('  \n')
mdFile.write('Align Text to center', align='center')
mdFile.write('  \n')


# Create Table
mdFile.new_header(level=1, title='TABLE EXAMPLE', header_id='table')
list_of_strings = ["Items", "Descriptions", "Data"]
for x in range(5):
	list_of_strings.extend(["Item " + str(x), "Description Item " + str(x), str(x)])
mdFile.new_line()
mdFile.new_table(columns=3, rows=6, text=list_of_strings, text_align='center')
mdFile.write('  \n')


# Create inline links
mdFile.new_header(level=1, title='INLINE LINKS EXAMPLE', header_id='inlinelinks')
mdFile.new_line('  - Inline link: ' + mdFile.new_inline_link(link='https://github.com/didix21/mdutils', text='mdutils'))
mdFile.new_line('  - Bold inline link: ' + mdFile.new_inline_link(link='https://github.com/didix21/mdutils', text='mdutils', bold_italics_code='b'))
mdFile.new_line('  - Italics inline link: ' + mdFile.new_inline_link(link='https://github.com/didix21/mdutils', text='mdutils', bold_italics_code='i'))
mdFile.new_line('  - Code inline link: ' + mdFile.new_inline_link(link='https://github.com/didix21/mdutils', text='mdutils', bold_italics_code='i')) 
mdFile.new_line('  - Bold italics code inline link: ' + mdFile.new_inline_link(link='https://github.com/didix21/mdutils', text='mdutils', bold_italics_code='cbi'))
mdFile.new_line('  - Another inline link: ' + mdFile.new_inline_link(link='https://github.com/didix21/mdutils'))
mdFile.write('  \n')


# Create referenced links
mdFile.new_header(level=1, title='REFERENCED LINKS EXAMPLE', header_id='referencedlinks')
mdFile.write('\n  - Reference link: ' + mdFile.new_reference_link(link='https://github.com/didix21/mdutils', text='mdutils', reference_tag='1'))
mdFile.write('\n  - Reference link: ' + mdFile.new_reference_link(link='https://github.com/didix21/mdutils', text='another reference', reference_tag='md'))
mdFile.write('\n  - Bold link: ' + mdFile.new_reference_link(link='https://github.com/didix21/mdutils', text='Bold reference', reference_tag='bold', bold_italics_code='b'))
mdFile.write('\n  - Italics link: ' + mdFile.new_reference_link(link='https://github.com/didix21/mdutils', text='Bold reference', reference_tag='italics', bold_italics_code='i'))
mdFile.write('  \n')


# Create list
mdFile.new_header(level=1, title='LIST EXAMPLE', header_id='list')
items = ['Item 1', 'Item 2', 'Item 3', 'Item 4', ['Item 4.1', 'Item 4.2', ['Item 4.2.1', 'Item 4.2.2'], 'Item 4.3', ['Item 4.3.1']], 'Item 5']
mdFile.new_list(items)


# Create ordered list
mdFile.new_header(level=1, title='ORDERED LIST EXAMPLE', header_id='orderedlist')
items = ['Item 1', 'Item 2', ['1. Item 2.1', '2. Item 2.2'], 'Item 3']
mdFile.new_list(items)
mdFile.new_list(items, marked_with='*')
mdFile.new_checkbox_list(items)
mdFile.new_checkbox_list(items, checked=True)
items = ['Item 1', 'Item 2', ['Item 2.1', 'x Item 2.2'], 'x Item 3']
mdFile.new_checkbox_list(items)


# Add images
# mdFile.new_header(level=1, title='IMAGES EXAMPLE', header_id='images')
# mdFile.new_line(mdFile.new_inline_image(text='snow trees', path='./doc/source/images/photo-of-snow-covered-trees.jpg'))


# Referenced images
# mdFile.new_header(level=1, title='REFERENCED IMAGES EXAMPLE', header_id='referencedimages')
# mdFile.new_line(mdFile.new_reference_image(text='snow trees', path='./doc/source/images/photo-of-snow-covered-trees.jpg', reference_tag='im'))


# HTML images
# mdFile.new_header(level=1, title='HTML IMAGES EXAMPLE', header_id='htmlimages')
# mdFile.new_paragraph(Html.image(path=path, size='200'))
# mdFile.new_paragraph(Html.image(path=path, size='x300'))
# mdFile.new_paragraph(Html.image(path=path, size='300x300'))
# mdFile.new_paragraph(Html.image(path=path, size='300x200', align='center'))




# Create header table with the headers 1 and 2 defined previously, this line must be called before created the file
mdFile.new_table_of_contents(table_title='Table of Contents example', depth=2)
### Create File
mdFile.create_md_file()


# Result


# Markdown file Example
# =====================

# # Header {#firstheader}

# Setext Header 1
# ===============

# Setext Header 2
# ---------------
# use the following available parameters:  
