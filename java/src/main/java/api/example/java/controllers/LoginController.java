package api.example.java.controllers;

import javax.servlet.http.HttpServletRequest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import api.example.java.api.ClimateOAuth;
import api.example.java.model.TokenResponse;

@Controller
public class LoginController extends BaseController{

	@Autowired
	private ClimateOAuth oAuth;

	@GetMapping("/login-redirect")
	public String loginRedirect(Model model, @RequestParam("code") String code, HttpServletRequest request) {
		model.addAttribute("code", code);

		TokenResponse tokenResponse = oAuth.getToken(code, request.getRequestURL().toString());
		saveTokenResponseInSession(request, tokenResponse);
		model.addAttribute("tokenResponse", tokenResponse);
		return "home";
	}

	@GetMapping("/refresh-token")
	public String refrshToken(Model model, @RequestParam("refresh_token") String refreshToken,
			HttpServletRequest request) {

		TokenResponse tokenResponse = oAuth.getRefreshToken(refreshToken);
		saveTokenResponseInSession(request, tokenResponse);
		model.addAttribute("tokenResponse", tokenResponse);
		return "home";
	}

	@GetMapping("/logout")
	public String logout(Model model, HttpServletRequest request) {
		cleanSession(request);
		return "redirect:/";
	}

}
