mkdir temp_pages

pdfseparate pages-odd-1-17.pdf temp_pages/odd-%d.pdf
pdfseparate pages-even-2-18.pdf temp_pages/even-%d.pdf

# Declare files as an empty array
files=()
for i in {1..9}; do
	files+=(temp_pages/odd-$i.pdf temp_pages/even-$i.pdf)
done

pdfunite $files all-pages-1-18.pdf


rm -rf temp_pages
