package api.example.java.controllers;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController extends BaseController{


	@GetMapping("/")
	public String home(Model model, HttpSession session, HttpServletRequest request) {

		if (isUserLoggedIn(session)) {
			return "home";
		}
		model.addAttribute("loginUri", config.buildOauthLink(request.getRequestURL().toString()));
		return "index";
	}
}
