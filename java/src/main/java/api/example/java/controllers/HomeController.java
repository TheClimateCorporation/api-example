package api.example.java.controllers;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController extends BaseController {
    private static final String LOGIN_URI = "loginUri";
    @GetMapping("/")
    public String home(Model model, HttpSession session, HttpServletRequest request) {
        if (isUserLoggedIn(session)) {
            return HOME_PAGE;
        }
        model.addAttribute(LOGIN_URI, config.buildOauthLink(request.getRequestURL().toString()));
        return INDEX_PAGE;
    }
}
