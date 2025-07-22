# This is a prompt file designed to guide and support the automation of an entire workflow.
# By following the prompts provided in this file, you can complete each step in sequence, enabling seamless process execution and automatic requirement completion.
# This file is applicable to various stages such as requirement analysis, workflow design, and execution validation, ensuring that tasks are carried out efficiently, systematically, and in an organized manner.

# Use Case Modeling Prompt
def generate_use_case_model(self, system_intro, data_entities, use_case_description):
    full_use_case_model_prompt = """
    ·You are responsible for use case modeling and validation in the requirements team.  
    ·System Overview: {intro}  
    ·Data Entities: {entities}  
    ·Use Cases: {use_cases}
    
    ·Task Steps:
        (a) Identify primary actors: Determine key roles involved in each use case.  
        (b) Specify preconditions and postconditions: Clearly define what must be true before the use case begins and the expected system state after it ends.  
        (c) Describe the main and alternate flows: Provide a logical sequence of steps for normal execution and identify alternative scenarios.  
        (d) Ensure completeness: Every use case from the list must be described fully with no omissions, and all actors should have reasonable interactions.
    ·Make sure:
        - Every use case listed is described.
        - No invented roles or use cases are introduced.
        - Language is clear, concise, and precise.
    
    ·Output Format:
        Use the following structure for each use case:
    
        === Use Case: <Use Case Name> ===  
        Primary Actor(s): <List of actors>  
        Preconditions: <State before execution>  
        Postconditions: <State after execution>  
        Main Flow:
          1. <Step 1>
          2. <Step 2>
          ...
    Alternate Flow(s):
      - <Alternative scenario 1>
      - <Alternative scenario 2>
    ===============================
    """

    prompt = full_use_case_model_prompt.format(
        intro=system_intro,
        entities=data_entities,
        use_cases=use_case_description
    )

    response = self.generate_response(prompt)

    try:
        self.use_case_model = response
        self.memory.append({"role": "assistant", "content": self.use_case_model})
        return self.use_case_model
    except AttributeError as e:
        return f"Error handling response: {str(e)}"

# Generate_CURD Prompt
def generate_er_model(self, system_intro, data_entities, use_cases):
    """Generate E-R model based on data entities"""
    self.system_intro = system_intro
    self.use_cases = use_cases
    self.data_entities = data_entities
    self.memory.append({"role": "user", "content": f"Data Entities: {data_entities}"})

    er_system_message = """
    ·You are responsible for data model design and validation in a requirements team. Based on the following information, please build a complete E-R model.
    ·System introduction: {input}
    ·Data entities: {en}
    ·Use cases: {uc}
    ·Please generate a complete E-R model based on the relationships among data entities.
    
        ·Thinking steps:
            1. Identify relationships using common sense: Analyze the business scenario and apply domain knowledge to identify relationships among entities.
            2. Supplement missing entities: Infer potentially missing entities and define their associations. E.g., for "User posts Review", add entity "ReviewRecord".
            3. Connectivity check and optimization: Ensure the model is at least a weakly connected graph. Address isolated entities by linking or merging where necessary.
            4. Output the complete data model: Include all entities (including added ones), their attributes, and relationships. At the end, list newly added or removed entities and corresponding use cases.

        ·Rules:
            1. Comprehensive entity recognition: Cover all extracted entities, and supplement missing ones as needed (within scope).
            2. Use case updates: Add management use cases for new entities. Indicate removals when entities are deleted or merged.
            3. Relationships must be logical and business-driven.
            4. Relationship completeness: Consider all direct and indirect relations.
            5. Model connectivity: Ensure no isolated entities.
            6. Output rules: Newly added entities and use cases should be listed using comma delimiters only, with no additional explanation.

        ·Example Output:
            1. Entity Relationship Recognition:
            - **Student** and **Book**: Borrow
            - **Admin** and **Book**: Manage
            - **Book** and **Subject**: Belongs to

            2. Inferred Missing Entities:
            - **BorrowRecord**: Tracks book borrowing by students

            3. Final ER Model:
            Entities and Attributes:
            1. **Student**: StudentID, Name, Age, Class
            2. **Book**: BookID, Title, Author, SubjectID, Status
            3. **Admin**: AdminID, Name, Role
            4. **Subject**: SubjectID, Name
            5. **BorrowRecord**: RecordID, StudentID, BookID, BorrowDate, ReturnDate

            Relationships:
            - Student "1" --> "0..*" BorrowRecord : borrows
            - Admin "1" --> "0..*" Book : manages
            - Book "1" --> "1" Subject : belongs to
            - Book o--* BorrowRecord : is borrowed

            New Entities: ReviewRecord, ApplicationResult, Post
            New Use Cases: Manage ReviewRecord, Manage ApplicationResult, Manage Post
        """
    prompt = er_system_message.format(input=system_intro, en=",".join(data_entities), uc=",".join(use_cases))
    response = self.generate_response(user_input=prompt)

    try:
        self.er_model = response
        self.memory.append({"role": "assistant", "content": self.er_model})
        return self.er_model
    except AttributeError as e:
        return f"Error processing response: {str(e)}"

# Generate CURD Matrix Prompt
def generate_curd_triples(self, data_entities, use_cases, use_case_description):
        self.memory.append({"role": "user", "content": f"Data_Entities：{data_entities}；Use_Cases：{use_cases}"})
        system_message = """
        · The data entities are as follows: {entities}
        · The use cases are as follows: {use_cases}
        · The use case descriptions are as follows: {uc_description}
        · Please output a structured list of triples (Entity, Use_case, CURD operation) based on the following rules:
            - C (Create): When the use case involves adding new data for the entity.
            - U (Update): When the use case involves modifying existing data for the entity.
            - R (Read): When the use case involves querying existing data for the entity.
            - D (Delete): When the use case involves deleting data for the entity.
        · Each use case for each entity may correspond to multiple CURD operations, which must be listed completely.
        · Note that if a use case only manages an entity, it includes C, R, U, and D operations.
        · If a use case is not related to an entity, do not generate a triple for that entity.
        · Output format should be a Python list, for example:
        [
            ("Task", "View Project", "R"),
            ("Project", "Manage Project", "R"),
            ("Project", "Manage Project", "U"),
            ("Project", "Manage Project", "D"),
            ("Task", "Delete Task", "D"),
            ("Project", "Manage Project", "C"),
        ]
        · Please return only the list of triples without any explanations or natural language text.
        """
        prompt = system_message.format(entities=data_entities, use_cases=use_cases, uc_description=use_case_description)
        response = self.generate_response(prompt)

        try:
            curd_triples = response.strip()
            self.memory.append({"role": "assistant", "content": str(curd_triples)})
            return curd_triples
        except Exception as e:
            return f"Error：{str(e)}"

# Completeness Evaluation Prompt
def evaluate_crud_completeness(self, system_intro, crud_matrix_text):
    completeness_prompt = """
    ·You are tasked with evaluating the completeness of a system's CRUD matrix.  
    ·System Overview: {intro}  
    ·Constructed CRUD Matrix:  
    {crud_matrix}
    
    ·Evaluation Steps:
        1. Classify all entities into two categories:
            - External entities (e.g., third-party systems)
            - Internal entities (within the system boundary)
    
        2. For each internal entity:
            - Check if it includes all CRUD operations (Create, Read, Update, Delete).
            - If any operation is missing, output a message:
              Format: Entity "<EntityName>" is missing operation(s): <C/U/R/D>
    
        3. For each external entity:
            - Ensure there is at least one Read (R) operation.
            - If missing, output:
              Format: Entity "<EntityName>" is missing operation(s): R
    
        4. If all entities pass their respective criteria:
            - Output: Evaluation Result: Pass
    
    ·Output Format Example:
        - Entity "UserProfile" is missing operation(s): C
        - Entity "PartnerAPI" is missing operation(s): R
        - Evaluation Result: Pass  (only if all checks are satisfied)
    
    ·Rules:
        - Use concise and exact wording.
        - Do not invent entities not present in the CRUD matrix.
        - Each message must align with the criteria strictly.
    
    ·Start Evaluation Now:
        System: {intro}  
        CRUD Matrix:
    {crud_matrix}
    """

    prompt = completeness_prompt.format(
        intro=system_intro,
        crud_matrix=crud_matrix_text
    )

    response = self.generate_response(prompt)

    try:
        self.crud_eval_result = response
        self.memory.append({"role": "assistant", "content": self.crud_eval_result})
        return self.crud_eval_result
    except AttributeError as e:
        return f"Error handling response: {str(e)}"

# Use Case Model Completion
def generate_new_use_case(self, system_intro, data_entities, new_use_cases):
    if isinstance(new_use_cases, str):
        use_case_list = [uc.strip() for uc in new_use_cases.split(",")]
    else:
        use_case_list = new_use_cases

    for idx, use_case in enumerate(use_case_list, 1):
        prompt = f"""
        ·You are a senior system analyst. Please continue to supplement a new use case description based on the following:
        ·System description: {system_intro}
        ·Data entities: {','.join(data_entities)}
        ·Current use case descriptions (keep consistent style and format):
        {self.simple_uc.strip() if self.simple_uc else 'None'}
        ·New use case to be added: {use_case}
        ·Please only generate the complete description for the new use case, including:
                - Use Case Name
                - Use Case ID (format: UC-XX, increment automatically)
                - Actors
                - Preconditions
                - Postconditions
                - Main Flow
                - Alternative Flow
        ·Do not repeat existing content, only add the new use case.
        """

        response = self.generate_response_func(prompt)

        try:
            formatted_response = response.strip()
            self.simple_uc += f"\n\n{formatted_response}"
            self.memory.append({"role": "user", "content": prompt})
            self.memory.append({"role": "assistant", "content": formatted_response})
        except AttributeError as e:
            self.simple_uc += f"\n\n[{use_case}] generation failed: {str(e)}"

    return self.simple_uc

# E-R Diagram Completion
def complete_er_diagram(self, old_er_diagram, use_case_model):
    er_completion_prompt = """
    ·You are responsible for completing and correcting the system's E-R diagram based on new use case information.  
    
    ·Input:
        (a) Old E-R Diagram:
        {er_diagram}
    
        (b) New Use Case Model:
        {use_case_model}
    
    ·Task Instructions:
        1. Identify any **new data entities** introduced or implied by the use case model.
        2. Define **relationships**:
            - Between new entities
            - Between new entities and existing entities
            (Use context from use case descriptions)
        3. Detect **isolated entities** (i.e., entities not connected to any other).
        4. Delete isolated entities and remove any associated use cases from the model.
    
    ·Output Format:
        - Updated E-R Diagram
        - Updated Use Case Model
    
    ·Rules:
        - Do not invent entities not grounded in the use cases.
        - Ensure all use cases refer to entities that exist in the updated E-R diagram.
        - Relationships should be meaningful and based on real data interactions implied by the use cases.
        - Use clear naming and structure.
    
    ·Begin the update now using the provided content.
    """

    prompt = er_completion_prompt.format(
        er_diagram=old_er_diagram,
        use_case_model=use_case_model
    )

    response = self.generate_response(prompt)

    try:
        self.updated_er_and_usecase = response
        self.memory.append({"role": "assistant", "content": self.updated_er_and_usecase})
        return self.updated_er_and_usecase
    except AttributeError as e:
        return f"Error handling response: {str(e)}"

# CURD Matrix Completion
def complete_crud_triplets(self, entities, uc_description, crud_triplets, missing_report):
    crud_completion_prompt = """
    ·You are responsible for completing the system’s CRUD matrix based on recent updates to use cases and missing interaction reports.
    
    ·Input:
        (a) Data Entities:
        {entities}
    
        (b) Use Case Descriptions:
        {uc_description}
    
        (c) Previous CRUD Triplets:
        {crud_triplets}
    
        (d) Use Case Missing Report:
        {missing_report}
    
    ·Task Instructions:
        1. Read and understand the entity–use case interaction gaps mentioned in the Use Case Missing Report.
        2. Analyze updated Use Case Descriptions to detect any new interactions (C, R, U, D) between entities and use cases.
        3. Compare these findings with the Previous CRUD Triplets to determine what is already covered.
        4. Construct new CRUD triplets **only** for missing interactions.
        5. Do **not** repeat any existing triplets from the previous matrix.
    
    ·Rules:
        - Ensure that every triplet reflects a valid and grounded interaction in the use case descriptions.
        - Use consistent naming for both entities and use cases.
        - Do not invent any operations or assumptions not supported by the use cases.
    
    ·Output Format:
        Python list only, using the following structure:
        [("Entity", "UseCase", "Operation")]
    """

    prompt = crud_completion_prompt.format(
        entities=entities,
        uc_description=uc_description,
        crud_triplets=crud_triplets,
        missing_report=missing_report
    )

    response = self.generate_response(prompt)

    try:
        self.new_crud_triplets = response
        self.memory.append({"role": "assistant", "content": self.new_crud_triplets})
        return self.new_crud_triplets
    except AttributeError as e:
        return f"Error handling response: {str(e)}"


# Requirements Output Prompt
def generate_functional_requirements(self, system_intro, er_model, use_case_description):
    # self.memory.append(
    #     {"role": "user", "content": f"Simplified use case description: {use_case_description}"})

    full_use_case_message = """
    ·You are responsible for writing the software requirement specification (SRS) of Chapter 1: Functional Requirements.
    ·System description: {intro}
    ·Data model: {er}
    ·Use case description: {use_case}
    ·Steps:
        1. Clarify the functional scope by extracting core functions from use cases and data models.
        2. Clearly define each function, including description, input, and output.
        3. Ensure all references (inputs/outputs) are defined in the context.
        4. Each function must be feasible: inputs must allow transformation to outputs.
        5. Output format must follow the example strictly.
    ·Rules:
        1. Each function must state input, output, and description clearly.
        2. Content must align with use cases and data model — no invented functions.
        3. Feasibility and completeness must be guaranteed.
        4. All references must be defined; no undefined terms.
        5. Strictly follow the output format.

    ·Example format:
    1.1 Data Import Function  
        Function ID: FR-01  
        Description: Users can upload Excel files containing contract data. Batch import must be supported.  
        Input: Excel files (.xlsx) with fields like contract number, balance, overdue days, etc.  
        Output: Structured data stored in DB or temp storage.

    1.2 Data Cleaning Function  
        Function ID: FR-02  
        Description: Perform format checks, fill in missing values, and handle outliers.  
        Input: Imported data table.  
        Output: Cleaned data table.
    """
    prompt = full_use_case_message.format(
        intro=system_intro,
        er=er_model,
        use_case=use_case_description
    )

    response = self.generate_response(prompt)

    try:
        self.full_uc = response
        self.memory.append({"role": "assistant", "content": self.full_uc})
        return self.full_uc
    except AttributeError as e:
        return f"Error handling response: {str(e)}"