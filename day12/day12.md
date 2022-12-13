<main>
<article class="day-desc"><h2>--- Day 12: Hill Climbing Algorithm ---</h2><p>You try contacting the Elves using your <span title="When you look up the specs for your handheld device, every field just says &quot;plot&quot;.">handheld device</span>, but the river you're following must be too low to get a decent signal.</p>
<p>You ask the device for a heightmap of the surrounding area (your puzzle input). The heightmap shows the local area from above broken into a grid; the elevation of each square of the grid is given by a single lowercase letter, where <code>a</code> is the lowest elevation, <code>b</code> is the next-lowest, and so on up to the highest elevation, <code>z</code>.</p>
<p>Also included on the heightmap are marks for your current position (<code>S</code>) and the location that should get the best signal (<code>E</code>). Your current position (<code>S</code>) has elevation <code>a</code>, and the location that should get the best signal (<code>E</code>) has elevation <code>z</code>.</p>
<p>You'd like to reach <code>E</code>, but to save energy, you should do it in <em>as few steps as possible</em>. During each step, you can move exactly one square up, down, left, or right. To avoid needing to get out your climbing gear, the elevation of the destination square can be <em>at most one higher</em> than the elevation of your current square; that is, if your current elevation is <code>m</code>, you could step to elevation <code>n</code>, but not to elevation <code>o</code>. (This also means that the elevation of the destination square can be much lower than the elevation of your current square.)</p>
<p>For example:</p>
<pre><code><em>S</em>abqponm
abcryxxl
accsz<em>E</em>xk
acctuvwj
abdefghi
</code></pre>
<p>Here, you start in the top-left corner; your goal is near the middle. You could start by moving down or right, but eventually you'll need to head toward the <code>e</code> at the bottom. From there, you can spiral around to the goal:</p>
<pre><code>v..v&lt;&lt;&lt;&lt;
&gt;v.vv&lt;&lt;^
.&gt;vv&gt;E^^
..v&gt;&gt;&gt;^^
..&gt;&gt;&gt;&gt;&gt;^
</code></pre>
<p>In the above diagram, the symbols indicate whether the path exits each square moving up (<code>^</code>), down (<code>v</code>), left (<code>&lt;</code>), or right (<code>&gt;</code>). The location that should get the best signal is still <code>E</code>, and <code>.</code> marks unvisited squares.</p>
<p>This path reaches the goal in <code><em>31</em></code> steps, the fewest possible.</p>
<p><em>What is the fewest steps required to move from your current position to the location that should get the best signal?</em></p>
</article>
<p>Your puzzle answer was <code>425</code>.</p><article class="day-desc"><h2 id="part2">--- Part Two ---</h2><p>As you walk up the hill, you suspect that the Elves will want to turn this into a hiking trail. The beginning isn't very scenic, though; perhaps you can find a better starting point.</p>
<p>To maximize exercise while hiking, the trail should start as low as possible: elevation <code>a</code>. The goal is still the square marked <code>E</code>. However, the trail should still be direct, taking the fewest steps to reach its goal. So, you'll need to find the shortest path from <em>any square at elevation <code>a</code></em> to the square marked <code>E</code>.</p>
<p>Again consider the example from above:</p>
<pre><code><em>S</em>abqponm
abcryxxl
accsz<em>E</em>xk
acctuvwj
abdefghi
</code></pre>
<p>Now, there are six choices for starting position (five marked <code>a</code>, plus the square marked <code>S</code> that counts as being at elevation <code>a</code>). If you start at the bottom-left square, you can reach the goal most quickly:</p>
<pre><code>...v&lt;&lt;&lt;&lt;
...vv&lt;&lt;^
...v&gt;E^^
.&gt;v&gt;&gt;&gt;^^
&gt;^&gt;&gt;&gt;&gt;&gt;^
</code></pre>
<p>This path reaches the goal in only <code><em>29</em></code> steps, the fewest possible.</p>
<p><em>What is the fewest steps required to move starting from any square with elevation <code>a</code> to the location that should get the best signal?</em></p>
</article>
<p>Your puzzle answer was <code>418</code>.</p><p class="day-success">Both parts of this puzzle are complete! They provide two gold stars: **</p>
<p>At this point, you should <a href="/2022">return to your Advent calendar</a> and try another puzzle.</p>
<p>If you still want to see it, you can <a href="12/input" target="_blank">get your puzzle input</a>.</p>
<p>You can also <span class="share">[Share<span class="share-content">on
  <a href="https://twitter.com/intent/tweet?text=I%27ve+completed+%22Hill+Climbing+Algorithm%22+%2D+Day+12+%2D+Advent+of+Code+2022&amp;url=https%3A%2F%2Fadventofcode%2Ecom%2F2022%2Fday%2F12&amp;related=ericwastl&amp;hashtags=AdventOfCode" target="_blank">Twitter</a>
  <a href="javascript:void(0);" onclick="var mastodon_instance=prompt('Mastodon Instance / Server Name?'); if(typeof mastodon_instance==='string' &amp;&amp; mastodon_instance.length){this.href='https://'+mastodon_instance+'/share?text=I%27ve+completed+%22Hill+Climbing+Algorithm%22+%2D+Day+12+%2D+Advent+of+Code+2022+%23AdventOfCode+https%3A%2F%2Fadventofcode%2Ecom%2F2022%2Fday%2F12'}else{return false;}" target="_blank">Mastodon</a></span>]</span> this puzzle.</p>
</main>