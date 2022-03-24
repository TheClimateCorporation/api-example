package api.example.java.controllers;

import java.io.IOException;
import java.text.NumberFormat;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import api.example.java.api.ClimateAPIs;
import api.example.java.model.Activity;
import api.example.java.model.ActivityResult;

@Controller
public class AgronomicDataController extends BaseController {
    private static final String ACTIVITIES_PAGE = "activities";
    private static final String ACTIVITIES = ACTIVITIES_PAGE;
    private static final String DATA_TYPE = "dataType";
    private static final String ID = "id";
    private static final String DATA = "data";
    @Autowired
    private ClimateAPIs climateAPIs;
    private static Logger logger = LoggerFactory.getLogger(AgronomicDataController.class);

    @GetMapping("/agronomic")
    public String agronomicData(Model model, @RequestParam(DATA) String dataType, HttpServletRequest request) {
        logger.info("Listing agronomic {} data" + dataType);
        List<Activity> activities = new ArrayList<Activity>();
        Iterator<ActivityResult> activityIterator = climateAPIs.getActivityIterator(agronomicApiUri(dataType),
                getAccessTokenFromSession(request));
        while (activityIterator.hasNext()) {
            ActivityResult activityResult = activityIterator.next();
            if (activityResult != null) {
                List<Activity> activityList = activityResult.getResults();
                if (activityList != null) {
                    activities.addAll(activityList);
                }
            }
        }
        model.addAttribute(ACTIVITIES, activities);
        model.addAttribute(DATA_TYPE, dataType);
        return ACTIVITIES_PAGE;
    }

    @GetMapping("/agronomic-contents")
    public void agronomicDataContent(Model model, @RequestParam(DATA) String dataType, @RequestParam(ID) String id,
            @RequestParam("length") String length, HttpServletRequest request, HttpServletResponse response)
            throws IOException, ParseException {
        logger.info("Fetching contents of agronomic - {} - acitity id - {}  length - {}", dataType, id, length);
        Number number = NumberFormat.getNumberInstance(java.util.Locale.US).parse(length);
        response.setContentType(MediaType.APPLICATION_OCTET_STREAM_VALUE);
        response.setStatus(HttpServletResponse.SC_OK);
        response.addHeader(HttpHeaders.CONTENT_DISPOSITION,
                String.format("attachment; filename=\"%s_%s.zip\"", id, dataType));
        ServletOutputStream out = response.getOutputStream();
        Iterator<ByteArrayResource> contentItr = climateAPIs.getContentIterator(agronomicContentsApiUri(id, dataType),
                number.intValue(), getAccessTokenFromSession(request));
        while (contentItr.hasNext()) {
            ByteArrayResource buffer = contentItr.next();
            out.write(buffer.getByteArray());
        }
        out.flush();
        out.close();
    }

}
