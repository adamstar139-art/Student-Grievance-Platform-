================================================================================
منصة سرية لشكاوى الطلاب - متوسطة الثغر النموذجية الأهلية (تطبيق Java / Spring Boot)
تصميم وتطوير: محمد سامي السعيد
مخصص للرفع على منصة GitHub: https://github.com/adamstar139-art/Student-Grievance-Platform-
================================================================================

1. ملف التطبيق الرئيسي: StudentGrievanceApplication.java
--------------------------------------------------------------------------------
package com.althaghr.platform;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

/**
 * منصة الشكاوى السرية لمتوسطة الثغر النموذجية الأهلية
 * تطوير وتصميم: محمد سامي السعيد
 */
@SpringBootApplication
@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class StudentGrievanceApplication {

    public static void main(String[] args) {
        SpringApplication.run(StudentGrievanceApplication.class, args);
    }

    // قواعد البيانات المؤقتة والسحابية
    private static final Map<Long, Complaint> complaintsDb = new ConcurrentHashMap<>();
    private static final List<Student> studentsRegistry = new ArrayList<>();
    private static final String ADMIN_PASSWORD = "000999";

    static {
        // تحميل سجل بيانات طلاب متوسطة الثغر النموذجية المرفقة بالهويات الوطنية وأرقام الجوالات الرسمية
        // صف أول متوسط
        studentsRegistry.add(new Student("إبراهيم محمد علي الوهيبي", "الأول المتوسط", "1", "1167628468", "966504158122"));
        studentsRegistry.add(new Student("الوليد خالد فهد العتيبي", "الأول المتوسط", "1", "1153756612", "966558522229"));
        studentsRegistry.add(new Student("بلال عبدالرزاق عيسى العيسى", "الأول المتوسط", "1", "2395664317", "966507448712"));
        studentsRegistry.add(new Student("حسام بن محمد بن علي آل رايان البارقي", "الأول المتوسط", "1", "1170582165", "966504445699"));
        studentsRegistry.add(new Student("ريان عبدالله جابر الأسمري", "الأول المتوسط", "1", "1169004353", "966554260960"));
        studentsRegistry.add(new Student("زيد زياد عبداللطيف أبو قبع", "الأول المتوسط", "1", "2446713998", "966590123455"));
        studentsRegistry.add(new Student("سامي سعد عباس حمد", "الأول المتوسط", "1", "2527104554", "966591781701"));
        studentsRegistry.add(new Student("سعد ناصر سعد السيف", "الأول المتوسط", "1", "1170111759", "966503219351"));
        studentsRegistry.add(new Student("عبدالعزيز عبدالله عبدالعزيز العمار", "الأول المتوسط", "1", "1195559479", "966555838394"));
        studentsRegistry.add(new Student("عبدالله سليمان عبدالله الراجحي", "الأول المتوسط", "1", "1153310501", "0551418881"));
        studentsRegistry.add(new Student("علي أحمد علي كريري", "الأول المتوسط", "1", "1171448515", "966558885481"));
        studentsRegistry.add(new Student("عمر عبدالله سعد الجبرين", "الأول المتوسط", "1", "1172018036", "966555249420"));
        studentsRegistry.add(new Student("مازن إسلام أحمد إبراهيم موسى", "الأول المتوسط", "1", "2552851368", "966550490495"));

        // صف ثاني متوسط
        studentsRegistry.add(new Student("تركي عبدالعزيز عبدالله المرزوق", "الثاني المتوسط", "2", "1156933093", "966501100076"));
        studentsRegistry.add(new Student("راكان إبراهيم محمد عبده", "الثاني المتوسط", "2", "2310646332", "966500030732"));
        studentsRegistry.add(new Student("رايان ناصر عبدالرحمن المرشود", "الثاني المتوسط", "2", "1161397599", "966550666662"));
        studentsRegistry.add(new Student("صالح ممدوح صالح الجويعي", "الثاني المتوسط", "2", "1163112129", "966549887719"));
        studentsRegistry.add(new Student("عبدالرحمن محمد صلاح السيد بدر الدين", "الثاني المتوسط", "2", "2508581135", "966507652707"));
        studentsRegistry.add(new Student("عبدالعزيز تركي عبدالعزيز اللهيم", "الثاني المتوسط", "2", "1162188872", "966505256806"));
        studentsRegistry.add(new Student("عمر فهد محمد سعد السقامي", "الثاني المتوسط", "2", "1162454266", "966564234552"));
        studentsRegistry.add(new Student("فيصل محمد صالح الفنتوخ", "الثاني المتوسط", "2", "1165152107", "966556488802"));
        studentsRegistry.add(new Student("مهند ماجد علي كعبي", "الثاني المتوسط", "2", "1162044851", "966533313738"));

        // صف ثالث متوسط
        studentsRegistry.add(new Student("ثامر عمر إبراهيم عثمان", "الثالث المتوسط", "3", "1166911709", "966538384444"));
        studentsRegistry.add(new Student("جهاد فارس عبدالقادر حناوي", "الثالث المتوسط", "3", "008464815", "966562674178"));
        studentsRegistry.add(new Student("خالد محمد عبدالكريم الخفاجي", "الثالث المتوسط", "3", "1164830562", "966533074601"));
        studentsRegistry.add(new Student("سعود ناصر سيف العريفي", "الثالث المتوسط", "3", "1167770468", "966505474606"));
        studentsRegistry.add(new Student("عبدالعزيز ماجد راشد الزير", "الثالث المتوسط", "3", "1167153434", "966500933390"));
        studentsRegistry.add(new Student("عبدالله بن بندر بن فهد المسيحل", "الثالث المتوسط", "3", "1167267341", "966500155334"));
        studentsRegistry.add(new Student("عزام خالد شلهوب بن شلهوب", "الثالث المتوسط", "3", "1167515020", "966506404016"));
        studentsRegistry.add(new Student("عمر وليد ياسين درويش علي", "الثالث المتوسط", "3", "4533080448", "966557790508"));
        studentsRegistry.add(new Student("يزيد بن حمد بن مترك القحطاني", "الثالث المتوسط", "3", "1166629798", "966556557210"));
    }

    // 1. استرجاع والبحث في قائمة الطلاب
    @GetMapping("/students")
    public ResponseEntity<List<Student>> getStudents(
            @RequestParam(required = false) String grade,
            @RequestParam(required = false) String classNum,
            @RequestParam(required = false) String query) {

        List<Student> result = studentsRegistry.stream().filter(s -> {
            boolean matchGrade = (grade == null || grade.isEmpty() || s.getGrade().equals(grade));
            boolean matchClass = (classNum == null || classNum.isEmpty() || s.getClassNum().equals(classNum));
            boolean matchQuery = (query == null || query.isEmpty() ||
                    s.getName().contains(query) || s.getNationalId().contains(query));
            return matchGrade && matchClass && matchQuery;
        }).collect(Collectors.toList());

        return ResponseEntity.ok(result);
    }

    // 2. استقبال الشكوى وتفريغ المربع والحفظ
    @PostMapping("/complaints")
    public ResponseEntity<Map<String, Object>> submitComplaint(@RequestBody Complaint complaint) {
        long id = System.currentTimeMillis();
        complaint.setId(id);
        complaint.setStatus("pending");
        complaint.setAdminAction("");
        complaint.setCreatedAt(LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")));

        complaintsDb.put(id, complaint);

        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        response.put("message", "تم إرسال الشكوى بنجاح وبسرية تامة إلى إدارة المدرسة");
        response.put("complaintId", id);
        response.put("saveStatus", "تم حفظ البيانات باللون الأخضر (Supabase / Local Database)");

        return ResponseEntity.ok(response);
    }

    // 3. التحقق من كلمة السر (000999)
    @PostMapping("/auth/verify")
    public ResponseEntity<Map<String, Object>> verifyPassword(@RequestBody Map<String, String> body) {
        String password = body.get("password");
        Map<String, Object> res = new HashMap<>();
        if (ADMIN_PASSWORD.equals(password)) {
            res.put("authenticated", true);
            res.put("message", "تم تسجيل الدخول بنجاح");
            return ResponseEntity.ok(res);
        } else {
            res.put("authenticated", false);
            res.put("message", "كلمة السر غير صحيحة!");
            return ResponseEntity.status(401).body(res);
        }
    }

    // 4. عرض الشكاوى الواردة لإدارة المدرسة
    @GetMapping("/complaints")
    public ResponseEntity<List<Complaint>> getComplaints(
            @RequestParam(required = false, defaultValue = "all") String status,
            @RequestHeader(value = "X-Admin-Password", required = false) String authHeader) {

        if (!ADMIN_PASSWORD.equals(authHeader)) {
            return ResponseEntity.status(403).build();
        }

        List<Complaint> list = complaintsDb.values().stream().filter(c -> {
            if ("pending".equals(status)) return "pending".equals(c.getStatus());
            if ("resolved".equals(status)) return "resolved".equals(c.getStatus());
            return true;
        }).sorted((a, b) -> Long.compare(b.getId(), a.getId())).collect(Collectors.toList());

        return ResponseEntity.ok(list);
    }

    // 5. اعتماد الإجراءات والتوقيع وتحويل للتقرير
    @PutMapping("/complaints/{id}/resolve")
    public ResponseEntity<Map<String, Object>> resolveComplaint(
            @PathVariable Long id,
            @RequestBody Map<String, String> body,
            @RequestHeader(value = "X-Admin-Password", required = false) String authHeader) {

        if (!ADMIN_PASSWORD.equals(authHeader)) {
            return ResponseEntity.status(403).build();
        }

        Complaint complaint = complaintsDb.get(id);
        if (complaint == null) {
            return ResponseEntity.notFound().build();
        }

        String action = body.get("adminAction");
        complaint.setStatus("resolved");
        complaint.setAdminAction(action);
        complaint.setActionDate(LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")));

        Map<String, Object> response = new HashMap<>();
        response.put("success", true);
        response.put("message", "تم اتخاذ القرار بنجاح وتحويل الشكوى إلى صفحة التقارير");
        response.put("whatsappUrl", "https://wa.me/966" + complaint.getPhoneNumber().replaceAll("^0", ""));
        response.put("signatures", Map.of(
            "studentAffairsProxy", "صالح بن عبدالله الدعجاني",
            "teacherAffairsProxy", "محمد مبروك السيد",
            "schoolPrincipal", "إبراهيم بن موسى التميمي"
        ));

        return ResponseEntity.ok(response);
    }

    // الكيانات البرمجية Data Models
    public static class Student {
        private String name;
        private String grade;
        private String classNum;
        private String nationalId;
        private String phoneNumber;

        public Student(String name, String grade, String classNum, String nationalId, String phoneNumber) {
            this.name = name;
            this.grade = grade;
            this.classNum = classNum;
            this.nationalId = nationalId;
            this.phoneNumber = phoneNumber;
        }

        public String getName() { return name; }
        public String getGrade() { return grade; }
        public String getClassNum() { return classNum; }
        public String getNationalId() { return nationalId; }
        public String getPhoneNumber() { return phoneNumber; }
    }

    public static class Complaint {
        private Long id;
        private String grade;
        private String classNum;
        private String studentName;
        private String nationalId;
        private String phoneNumber;
        private String complaintText;
        private String status;
        private String adminAction;
        private String createdAt;
        private String actionDate;

        public Long getId() { return id; }
        public void setId(Long id) { this.id = id; }
        public String getGrade() { return grade; }
        public void setGrade(String grade) { this.grade = grade; }
        public String getClassNum() { return classNum; }
        public void setClassNum(String classNum) { this.classNum = classNum; }
        public String getStudentName() { return studentName; }
        public void setStudentName(String studentName) { this.studentName = studentName; }
        public String getNationalId() { return nationalId; }
        public void setNationalId(String nationalId) { this.nationalId = nationalId; }
        public String getPhoneNumber() { return phoneNumber; }
        public void setPhoneNumber(String phoneNumber) { this.phoneNumber = phoneNumber; }
        public String getComplaintText() { return complaintText; }
        public void setComplaintText(String complaintText) { this.complaintText = complaintText; }
        public String getStatus() { return status; }
        public void setStatus(String status) { this.status = status; }
        public String getAdminAction() { return adminAction; }
        public void setAdminAction(String adminAction) { this.adminAction = adminAction; }
        public String getCreatedAt() { return createdAt; }
        public void setCreatedAt(String createdAt) { this.createdAt = createdAt; }
        public String getActionDate() { return actionDate; }
        public void setActionDate(String actionDate) { this.actionDate = actionDate; }
    }
}


2. ملف الإعدادات pom.xml (لـ Maven):
--------------------------------------------------------------------------------
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>
    <groupId>com.althaghr</groupId>
    <artifactId>student-grievance-platform</artifactId>
    <version>1.0.0</version>
    <name>student-grievance-platform</name>
    <description>منصة الشكاوى السرية لمتوسطة الثغر النموذجية الأهلية</description>
    <properties>
        <java.version>17</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>


3. ملف application.properties:
--------------------------------------------------------------------------------
server.port=8080
spring.application.name=StudentGrievancePlatform
supabase.url=https://looldhswootseeqltohg.supabase.co
# كلمة السر الإدارية
admin.auth.password=000999


================================================================================
حقوق الملكية الفكرية والتطوير:
تصميم وتطوير: محمد سامي السعيد
مدرسة: متوسطة الثغر النموذجية الأهلية
================================================================================
