from bs4 import BeautifulSoup


def getContext(html,n):
    output = []
    soup = BeautifulSoup(html, 'html.parser')
    for i in soup.findAll("span"):
        n_side = int(n/2)

        text = soup.text.replace('\n',' ')

        context_before = text.split(i.text)[0]
        words_before = list(filter(bool,context_before.split(" ")))

        context_after = text.split(i.text)[1]
        words_after = list(filter(bool,context_after.split(" ")))

        if(len(words_after) >= n_side):
            words_before = words_before[-n_side:]
            words_after = words_after[:(n-len(words_before))]
        else:
            words_after = words_after[:n_side]
            words_before = words_before[-(n-len(words_after)):]

        output.append(words_before + words_after)
    return output


html = '''<html><body>
<p>Assuming this is relative to the origin (as John pointed out): Given two position
 vectors <span class="math-container" id="917">\vec p_1</span> and
  <span class="math-container" id="918">\vec p_2</span>, their dot product is:</p> 
  <p><span class="math-container" id="919">\vec p_1\cdot \vec p_2 = |\vec p_1| \cdot |\vec p_2| \cdot \cos \theta</span></p> 
  <p>Solving for <span class="math-container" id="920">\theta</span>, we get:</p> 
  <p><span class="math-container" id="921">\theta = \arccos\left(\frac{\vec p_1 \cdot \vec p_2}{|\vec p_1| \cdot |\vec p_2|}\right)</span></p> 
  <p>In a 2D space this equals:</p> <p><span class="math-container" id="922">v=\arccos\left(\frac{x_1x_2 + y_1y_2}{\sqrt{(x_1^2+y_1^2)\cdot(x_2^2+y_2^2)}}\right)</span></p> 
  <p>And extended for 3D space:</p> <p><span class="math-container" id="923">v=\arccos\left(\frac{x_1x_2 + y_1y_2 + z_1z_2}{\sqrt{(x_1^2+y_1^2+z_1^2)\cdot(x_2^2+y_2^2+z_2^2)}}\right)</span></p> 
</body></html>'''

html1 = '''<html><body>
<p>Given two position
 vectors <span class="math-container" id="917">\vec p_1</span> and their dot product is:</p> 
  <p>In a 2D space this equals:</p> <p><span class="math-container" id="922">v=\arccos\left(\frac{x_1x_2 + y_1y_2}{\sqrt{(x_1^2+y_1^2)\cdot(x_2^2+y_2^2)}}\right)</span></p> 
  <p>And extended for 3D space:</p> <p><span class="math-container" id="923">v=\arccos\left(\frac{x_1x_2 + y_1y_2 + z_1z_2}{\sqrt{(x_1^2+y_1^2+z_1^2)\cdot(x_2^2+y_2^2+z_2^2)}}\right)</span></p> 
</body></html>'''

print(*getContext(html1,8))

