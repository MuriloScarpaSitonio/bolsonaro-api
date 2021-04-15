const BASE_API_URL = process.env.REACT_APP_BASE_API_URL || "http://127.0.0.1:8000/api/v1"
const ADMIN_EMAIL = "bolsonaroapi@gmail.com"
const SITE_URL = "http://bolsonaro-api.herokuapp.com"
const _TEST_RECAPTCHA_SITE_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
//https://developers.google.com/recaptcha/docs/faq#id-like-to-run-automated-tests-with-recaptcha.-what-should-i-do
const RECAPTCHA_SITE_KEY = process.env.REACT_APP_RECAPTCHA_SITE_KEY || _TEST_RECAPTCHA_SITE_KEY
const PIX_KEY = process.env.REACT_APP_PIX_KEY || ""

export {ADMIN_EMAIL,BASE_API_URL,RECAPTCHA_SITE_KEY,SITE_URL,PIX_KEY}
