import com.google.gson.Gson;

public class GsonExample {
    static class Person {
        private String name;
        private int age;

        // 构造函数
        public Person(String name, int age) {
            this.name = name;
            this.age = age;
        }

        // toString 方法方便打印结果
        @Override
        public String toString() {
            return "Person{name='" + name + "', age=" + age + "}";
        }
    }
    public static void main(String[] args) {
        // 创建 Gson 实例
        Gson gson = new Gson();

        // 要序列化的对象
        Person person = new Person("Alice", 30);

        // 序列化为 JSON 字符串
        String json = gson.toJson(person);
        System.out.println("Serialized JSON: " + json); 
        // 输出: {"name":"Alice","age":30}

        // 反序列化回 Java 对象
        Person deserializedPerson = gson.fromJson(json, Person.class);
        System.out.println("Deserialized Object: " + deserializedPerson);
        // 输出: Person{name='Alice', age=30}
    }
}