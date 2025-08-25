// Adapted from https://codepen.io/vuong_huu_thien/pen/odjrXq
document.addEventListener('DOMContentLoaded', function() {
    var emailLabel = document.querySelector('label[for="id_username"]'),
        email = document.querySelector('#id_username'),
        passwordLabel = document.querySelector('label[for="id_password"]'),
        password = document.querySelector('#id_password'),
        showPasswordCheck = document.querySelector('#showPasswordCheck'),
        mySVG = document.querySelector('.svgContainer'),
        twoFingers = document.querySelector('.twoFingers'),
        armL = document.querySelector('.armL'),
        armR = document.querySelector('.armR'),
        eyeL = document.querySelector('.eyeL'),
        eyeR = document.querySelector('.eyeR'),
        nose = document.querySelector('.nose'),
        mouth = document.querySelector('.mouth'),
        mouthBG = document.querySelector('.mouthBG'),
        mouthSmallBG = document.querySelector('.mouthSmallBG'),
        mouthMediumBG = document.querySelector('.mouthMediumBG'),
        mouthLargeBG = document.querySelector('.mouthLargeBG'),
        mouthMaskPath = document.querySelector('#mouthMaskPath'),
        mouthOutline = document.querySelector('.mouthOutline'),
        tooth = document.querySelector('.tooth'),
        tongue = document.querySelector('.tongue'),
        chin = document.querySelector('.chin'),
        face = document.querySelector('.face'),
        eyebrow = document.querySelector('.eyebrow'),
        outerEarL = document.querySelector('.earL .outerEar'),
        outerEarR = document.querySelector('.earR .outerEar'),
        earHairL = document.querySelector('.earL .earHair'),
        earHairR = document.querySelector('.earR .earHair'),
        hair = document.querySelector('.hair'),
        bodyBG = document.querySelector('.bodyBGnormal'),
        bodyBGchanged = document.querySelector('.bodyBGchanged');

    var activeElement, curEmailIndex, screenCenter, svgCoords, emailCoords, emailScrollMax, chinMin = .5, dFromC, mouthStatus = "small", blinking, eyeScale = 1, eyesCovered = false;
    var eyeLCoords, eyeRCoords, noseCoords, mouthCoords, eyeLAngle, eyeLX, eyeLY, eyeRAngle, eyeRX, eyeRY, noseAngle, noseX, noseY, mouthAngle, mouthX, mouthY, mouthR, chinX, chinY, chinS, faceX, faceY, faceSkew, eyebrowSkew, outerEarX, outerEarY, hairX, hairS;

    if (!email) return; // Don't run if the form isn't on the page

    function calculateFaceMove(e) {
        var
            carPos = email.selectionEnd,
            div = document.createElement('div'),
            span = document.createElement('span'),
            copyStyle = getComputedStyle(email),
            caretCoords = {};
        ;
        if (carPos == null || carPos == 0) {
            carPos = email.value.length;
        }
        [].forEach.call(copyStyle, function(prop) {
            div.style[prop] = copyStyle[prop];
        });
        div.style.position = 'absolute';
        document.body.appendChild(div);
        div.textContent = email.value.substr(0, carPos);
        span.textContent = email.value.substr(carPos) || '.';
        div.appendChild(span);

        if (email.scrollWidth <= emailScrollMax) {
            caretCoords = getPosition(span);
            dFromC = screenCenter - (caretCoords.x + emailCoords.x);
            eyeLAngle = getAngle(eyeLCoords.x, eyeLCoords.y, emailCoords.x + caretCoords.x, emailCoords.y + 25);
            eyeRAngle = getAngle(eyeRCoords.x, eyeRCoords.y, emailCoords.x + caretCoords.x, emailCoords.y + 25);
            noseAngle = getAngle(noseCoords.x, noseCoords.y, emailCoords.x + caretCoords.x, emailCoords.y + 25);
            mouthAngle = getAngle(mouthCoords.x, mouthCoords.y, emailCoords.x + caretCoords.x, emailCoords.y + 25);
        } else {
            eyeLAngle = getAngle(eyeLCoords.x, eyeLCoords.y, emailCoords.x + emailScrollMax, emailCoords.y + 25);
            eyeRAngle = getAngle(eyeRCoords.x, eyeRCoords.y, emailCoords.x + emailScrollMax, emailCoords.y + 25);
            noseAngle = getAngle(noseCoords.x, noseCoords.y, emailCoords.x + emailScrollMax, emailCoords.y + 25);
            mouthAngle = getAngle(mouthCoords.x, mouthCoords.y, emailCoords.x + emailScrollMax, emailCoords.y + 25);
        }

        eyeLX = Math.cos(eyeLAngle) * 20;
        eyeLY = Math.sin(eyeLAngle) * 10;
        eyeRX = Math.cos(eyeRAngle) * 20;
        eyeRY = Math.sin(eyeRAngle) * 10;
        noseX = Math.cos(noseAngle) * 23;
        noseY = Math.sin(noseAngle) * 10;
        mouthX = Math.cos(mouthAngle) * 23;
        mouthY = Math.sin(mouthAngle) * 10;
        mouthR = Math.cos(mouthAngle) * 6;
        chinX = mouthX * .8;
        chinY = mouthY * .5;
        chinS = 1 - ((dFromC * .15) / 100);
        if (chinS > 1) {
            chinS = 1 - (chinS - 1);
            if (chinS < chinMin) {
                chinS = chinMin;
            }
        }
        faceX = mouthX * .3;
        faceY = mouthY * .4;
        faceSkew = Math.cos(mouthAngle) * 5;
        eyebrowSkew = Math.cos(mouthAngle) * 25;
        outerEarX = Math.cos(mouthAngle) * 4;
        outerEarY = Math.cos(mouthAngle) * 5;
        hairX = Math.cos(mouthAngle) * 6;
        hairS = 1.2;

        gsap.to(eyeL, 1, { x: -eyeLX, y: -eyeLY, ease: 'expo.out' });
        gsap.to(eyeR, 1, { x: -eyeRX, y: -eyeRY, ease: 'expo.out' });
        gsap.to(nose, 1, { x: -noseX, y: -noseY, rotation: mouthR, transformOrigin: "center center", ease: 'expo.out' });
        gsap.to(mouth, 1, { x: -mouthX, y: -mouthY, rotation: mouthR, transformOrigin: "center center", ease: 'expo.out' });
        gsap.to(chin, 1, { x: -chinX, y: -chinY, scaleY: chinS, ease: 'expo.out' });
        gsap.to(face, 1, { x: -faceX, y: -faceY, skewX: -faceSkew, transformOrigin: "center top", ease: 'expo.out' });
        gsap.to(eyebrow, 1, { x: -faceX, y: -faceY, skewX: -eyebrowSkew, transformOrigin: "center top", ease: 'expo.out' });
        gsap.to(outerEarL, 1, { x: outerEarX, y: -outerEarY, ease: 'expo.out' });
        gsap.to(outerEarR, 1, { x: outerEarX, y: outerEarY, ease: 'expo.out' });
        gsap.to(earHairL, 1, { x: -outerEarX, y: -outerEarY, ease: 'expo.out' });
        gsap.to(earHairR, 1, { x: -outerEarX, y: outerEarY, ease: 'expo.out' });
        gsap.to(hair, 1, { x: hairX, scaleY: hairS, transformOrigin: "center bottom", ease: 'expo.out' });

        document.body.removeChild(div);
    };

    function onEmailInput(e) {
        calculateFaceMove(e);
        var value = email.value;
        curEmailIndex = value.length;

        if (curEmailIndex > 0) {
            if (mouthStatus == "small") {
                mouthStatus = "medium";
                gsap.to([mouthBG, mouthOutline, mouthMaskPath], 1, { morphSVG: {shape: mouthMediumBG, shapeIndex: 8}, ease: 'expo.out' });
                gsap.to(tooth, 1, { x: 0, y: 0, ease: 'expo.out' });
                gsap.to(tongue, 1, { x: 0, y: 1, ease: 'expo.out' });
                gsap.to([eyeL, eyeR], 1, { scaleX: .85, scaleY: .85, ease: 'expo.out' });
                eyeScale = .85;
            }
            if (value.includes("@")) {
                mouthStatus = "large";
                gsap.to([mouthBG, mouthOutline, mouthMaskPath], 1, { morphSVG: {shape: mouthLargeBG}, ease: 'expo.out' });
                gsap.to(tooth, 1, { x: 3, y: -2, ease: 'expo.out' });
                gsap.to(tongue, 1, { y: 2, ease: 'expo.out' });
                gsap.to([eyeL, eyeR], 1, { scaleX: .65, scaleY: .65, ease: 'expo.out', transformOrigin: "center center" });
                eyeScale = .65;
            } else {
                if (mouthStatus == "large") {
                    mouthStatus = "medium";
                    gsap.to([mouthBG, mouthOutline, mouthMaskPath], 1, { morphSVG: {shape: mouthMediumBG}, ease: 'expo.out' });
                    gsap.to(tooth, 1, { x: 0, y: 0, ease: 'expo.out' });
                    gsap.to(tongue, 1, { x: 0, y: 1, ease: 'expo.out' });
                    gsap.to([eyeL, eyeR], 1, { scaleX: .85, scaleY: .85, ease: 'expo.out' });
                    eyeScale = .85;
                }
            }
        } else {
            mouthStatus = "small";
            gsap.to([mouthBG, mouthOutline, mouthMaskPath], 1, { morphSVG: {shape: mouthSmallBG, shapeIndex: 9}, ease: 'expo.out' });
            gsap.to(tooth, 1, { x: 0, y: 0, ease: 'expo.out' });
            gsap.to(tongue, 1, { y: 0, ease: 'expo.out' });
            gsap.to([eyeL, eyeR], 1, { scaleX: 1, scaleY: 1, ease: 'expo.out' });
            eyeScale = 1;
        }
    }

    function onEmailFocus(e) {
        activeElement = "email";
        e.target.parentElement.classList.add("focusWithText");
        onEmailInput();
    }

    function onEmailBlur(e) {
        activeElement = null;
        setTimeout(function() {
            if (activeElement != "email") {
                if (e.target.value == "") {
                    e.target.parentElement.classList.remove("focusWithText");
                }
                resetFace();
            }
        }, 100);
    }

    function onPasswordToggleChange(e) {
        setTimeout(function() {
            if (e.target.checked) {
                password.type = "text";
                spreadFingers();
            } else {
                password.type = "password";
                closeFingers();
            }
        }, 100);
    }

    function onPasswordFocus(e) {
        activeElement = "password";
        if (!eyesCovered) {
            coverEyes();
        }
    }

    function onPasswordBlur(e) {
        activeElement = null;
        setTimeout(function() {
            if (activeElement != "toggle" && activeElement != "password") {
                uncoverEyes();
            }
        }, 100);
    }

    function spreadFingers() {
        gsap.to(twoFingers, .35, { transformOrigin: "bottom left", rotation: 30, x: -9, y: -2, ease: 'power2.inOut' });
    }

    function closeFingers() {
        gsap.to(twoFingers, .35, { transformOrigin: "bottom left", rotation: 0, x: 0, y: 0, ease: 'power2.inOut' });
    }

    function coverEyes() {
        gsap.killTweensOf([armL, armR]);
        gsap.set([armL, armR], { visibility: "visible" });
        gsap.to(armL, .45, { x: -93, y: 10, rotation: 0, ease: 'quad.out' });
        gsap.to(armR, .45, { x: -93, y: 10, rotation: 0, ease: 'quad.out', delay: .1 });
        gsap.to(bodyBG, .45, { morphSVG: {shape: bodyBGchanged}, ease: 'quad.out' });
        eyesCovered = true;
    }

    function uncoverEyes() {
        gsap.killTweensOf([armL, armR]);
        gsap.to(armL, 1.35, { y: 220, ease: 'quad.out' });
        gsap.to(armL, 1.35, { rotation: 105, ease: 'quad.out', delay: .1 });
        gsap.to(armR, 1.35, { y: 220, ease: 'quad.out' });
        gsap.to(armR, 1.35, { rotation: -105, ease: 'quad.out', delay: .1, onComplete: function() {
            gsap.set([armL, armR], { visibility: "hidden" });
        }});
        gsap.to(bodyBG, .45, { morphSVG: {shape: bodyBG}, ease: 'quad.out' });
        eyesCovered = false;
    }

    function resetFace() {
        gsap.to([eyeL, eyeR], 1, { x: 0, y: 0, ease: 'expo.out' });
        gsap.to(nose, 1, { x: 0, y: 0, scaleX: 1, scaleY: 1, ease: 'expo.out' });
        gsap.to(mouth, 1, { x: 0, y: 0, rotation: 0, ease: 'expo.out' });
        gsap.to(chin, 1, { x: 0, y: 0, scaleY: 1, ease: 'expo.out' });
        gsap.to([face, eyebrow], 1, { x: 0, y: 0, skewX: 0, ease: 'expo.out' });
        gsap.to([outerEarL, outerEarR, earHairL, earHairR, hair], 1, { x: 0, y: 0, scaleY: 1, ease: 'expo.out' });
    }

    function getAngle(x1, y1, x2, y2) {
        var angle = Math.atan2(y1 - y2, x1 - x2);
        return angle;
    }

    function getPosition(el) {
        var xPos = 0;
        var yPos = 0;
        while (el) {
            if (el.tagName == "BODY") {
                var xScroll = el.scrollLeft || document.documentElement.scrollLeft;
                var yScroll = el.scrollTop || document.documentElement.scrollTop;
                xPos += (el.offsetLeft - xScroll + el.clientLeft);
                yPos += (el.offsetTop - yScroll + el.clientTop);
            } else {
                xPos += (el.offsetLeft - el.scrollLeft + el.clientLeft);
                yPos += (el.offsetTop - el.scrollTop + el.clientTop);
            }
            el = el.offsetParent;
        }
        return { x: xPos, y: yPos };
    }

    function initLoginForm() {
        svgCoords = getPosition(mySVG);
        emailCoords = getPosition(email);
        screenCenter = svgCoords.x + (mySVG.offsetWidth / 2);
        eyeLCoords = { x: svgCoords.x + 84, y: svgCoords.y + 76 };
        eyeRCoords = { x: svgCoords.x + 113, y: svgCoords.y + 76 };
        noseCoords = { x: svgCoords.x + 97, y: svgCoords.y + 81 };
        mouthCoords = { x: svgCoords.x + 100, y: svgCoords.y + 100 };

        email.addEventListener('focus', onEmailFocus);
        email.addEventListener('blur', onEmailBlur);
        email.addEventListener('input', onEmailInput);

        password.addEventListener('focus', onPasswordFocus);
        password.addEventListener('blur', onPasswordBlur);

        if(showPasswordCheck){
            showPasswordCheck.addEventListener('change', onPasswordToggleChange);
        }

        gsap.set(armL, { x: -93, y: 220, rotation: 105, transformOrigin: "top left" });
        gsap.set(armR, { x: -93, y: 220, rotation: -105, transformOrigin: "top right" });

        emailScrollMax = email.scrollWidth;
    }

    initLoginForm();
});
