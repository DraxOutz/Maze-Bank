console.log("Animação start")

// window.alert("Script rodando")
 // window.document.body

const banners = ["banner1", "banner2", "banner3"];
const texts = [
  { title: "Não se preocupe com as contas!", text: "Estamos aqui para te ajudar a planejar seus gastos com soluções que realmente funcionam para você." },
  { title: "Sua dívida tem solução!", text: "Conte com a gente para se organizar com ofertas que cabem no seu bolso." },
  { title: "Planeje seus gastos!", text: "Aproveite dicas e ofertas que facilitam sua vida financeira." }
];

let current = 0;

function changeBanner() {
  const prevImg = document.getElementById(banners[current]);

  // próxima imagem
  current = (current + 1) % banners.length;
  const nextImg = document.getElementById(banners[current]);

  // prepara a nova imagem vindo da direita
  nextImg.classList.add("active"); // entra da direita
  nextImg.style.transform = "translateX(100%)";

  // força o browser a aplicar a transformação antes da animação
  requestAnimationFrame(() => {
    nextImg.style.transform = "translateX(0)"; // anima para posição visível
    prevImg.style.transform = "translateX(-100%)"; // antiga vai para esquerda
  });

  // remove a antiga depois da animação
  setTimeout(() => {
    prevImg.classList.remove("active");
    prevImg.style.transform = ""; // reseta
  }, 800); // tempo da transição

  // atualiza o texto
  document.getElementById("banner-title").innerText = texts[current].title;
  document.getElementById("banner-text").innerText = texts[current].text;
}

setInterval(changeBanner, 5000);