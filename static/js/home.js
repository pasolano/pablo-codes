$(document).ready(function() {
  /* NOTE: hard-refresh the browser once you've updated this */
  $(".typed").typed({
    strings: [
      "stat pablo.human<br/>" + 
      "><span class='dollar'>$</span> career: associate software engineer @ riot games<br/> ^100" +
      "><span class='dollar'>$</span> team: the league engine // content workflows<br/> ^100" +
      "><span class='dollar'>$</span> socials: <a href='mailto:pablo.a.solano@gmail.com'>email</a>, <a href='http://www.github.com/pasolano/'>github</a>, <a href='http://in.linkedin.com/in/pabloadriansolano/'>linkedin</a><br/>" +
      "><span class='dollar'>$</span> school: computer science graduate ('22) from william &amp; mary<br/> ^100"
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

function close() {
  $('.terminal').hide();
  $('#dock').show();
}

function min() {
  $('.message').hide();
  $('.terminal').css('height', '30px');
}

function max() {
  $('.message').show();
  $('.terminal').css('height', '260px');
}

function moveLogo(amount) {
  $('#terminal-logo').animate({
    top: amount
  });
}

function openTerminal() {
  for (var i = 0; i < 3; i++) {
    moveLogo("-=60px");
    moveLogo("+=60px");
  }
  // hacky way to delay between bounce animation and opening terminal
  $('#terminal-logo').animate({
    top: "+=0px"
  }, 800, function() {
    $('#dock').hide();
    $('.terminal').show();
    max();
  });
}

console.log("the terminal supports some commands :)")