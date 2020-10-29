$(function() {
  /* NOTE: hard-refresh the browser once you've updated this */
  $(".typed").typed({
    strings: [
      "stat pablo.human<br/>" + 
      "><span class='caret'>$</span> school: computer science major at william & mary<br/> ^100" +
      "><span class='caret'>$</span> honors: <a href='https://www.wm.edu/as/1693scholars/current/solano_p/index.php'>stamps 1693 scholar</a>, william & mary scholar, james monroe scholar<br/>" +
      "><span class='caret'>$</span> languages: python, javascript, c++, java<br/> ^100" +
      "><span class='caret'>$</span> bilingual/biliterate: english/spanish<br/> ^300"/*
      "><span class='caret'>$</span> <a href='/timeline'>timeline</a> <a href='http://www.github.com/crearo/'>github</a> <a href='http://in.linkedin.com/in/bhardwajrish/'>linkedin</a> <a href='http://bhardwajrish.blogspot.com/'>blog</a><br/>"*/
    ],
    showCursor: true,
    cursorChar: '_',
    autoInsertCss: true,
    typeSpeed: 0.001,
    startDelay: 50,
    loop: false,
    showCursor: false,
    onStart: $('.message form').hide(),
    onStop: $('.message form').show(),
    onTypingResumed: $('.message form').hide(),
    onTypingPaused: $('.message form').show(),
    onComplete: $('.message form').show(),
    onStringTyped: function(pos, self) {$('.message form').show();},
  });
  $('.message form').hide()
});
