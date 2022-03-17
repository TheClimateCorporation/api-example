package api.example.java.controllers;

import javax.servlet.http.HttpServletRequest;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import api.example.java.api.ClimateAPIs;
@Controller
public class FieldController extends BaseController {

    private static final String FIELDS = "fields";

    private static final String FIELDS_PAGE = FIELDS;
    @Autowired
    private ClimateAPIs climateAPIs;
    private static Logger logger = LoggerFactory.getLogger(FieldController.class);

    @GetMapping("/fields")
    public String getFields(Model model, HttpServletRequest request) {
        logger.info("Fields controller entered");
        model.addAttribute(FIELDS, climateAPIs.getFields(fieldsApiUri(), getAccessTokenFromSession(request)).getResults());
        return FIELDS_PAGE;
    }
}
