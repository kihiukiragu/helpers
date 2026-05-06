# When you flipped the papers and scanned the even pages from the last even page to page 2
# Because you didn't want to disorganize the pile
mkdir -p temp_pages
pdfseparate pages-odd-1-17.pdf temp_pages/odd-%d.pdf
pdfseparate pages-even-2-18.pdf temp_pages/even-%d.pdf

files=() # Empty array
# We loop from 1 to 9
for i in {1..9}; do
  # Calculate the mirror index for the even pages: 10 - i
  # When i=1 (page 1), even_idx=9 (page 2) ... Wait, if page 18 is first:
  # If page 18 is the first page of the PDF, then even-1.pdf is page 18.
  # To get page 2, we need the last page of that file (even-9.pdf).

  even_idx=$((10 - i)) 
  files+=(temp_pages/odd-$i.pdf temp_pages/even-$even_idx.pdf)
done

pdfunite $files all-pages-1-18.pdf
